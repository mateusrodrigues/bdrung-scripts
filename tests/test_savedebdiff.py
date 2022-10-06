# Copyright (C) 2022, Benjamin Drung <bdrung@ubuntu.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

"""Test savedebdiff."""


import os
import tempfile
import unittest
import unittest.mock

import unidiff

from .scripts.savedebdiff import derive_filename_from_debdiff, main, save_debdiff

LIBEVENT_DEBDIFF = """\
diff -Nru libevent-2.1.12-stable/debian/changelog libevent-2.1.12-stable/debian/changelog
--- libevent-2.1.12-stable/debian/changelog	2022-04-15 17:26:52.000000000 +0200
+++ libevent-2.1.12-stable/debian/changelog	2022-10-05 19:13:56.000000000 +0200
@@ -1,3 +1,10 @@
+libevent (2.1.12-stable-5ubuntu1) kinetic; urgency=medium
+
+  * Bump soname for libevent and libevent-core to 2.1-7a for dropping
+    evutil_secure_rng_add_bytes (LP: #1990941)
+
+ -- Benjamin Drung <bdrung@ubuntu.com>  Wed, 05 Oct 2022 19:13:56 +0200
+
 libevent (2.1.12-stable-5) unstable; urgency=medium
 [trailing space protection]
   * d/control: Update maintainer
diff -Nru libevent-2.1.12-stable/debian/control libevent-2.1.12-stable/debian/control
--- libevent-2.1.12-stable/debian/control	2022-04-15 17:26:42.000000000 +0200
+++ libevent-2.1.12-stable/debian/control	2022-10-05 19:07:42.000000000 +0200
@@ -1,5 +1,6 @@
 Source: libevent
-Maintainer: Nicolas Mora <babelouest@debian.org>
+Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
+XSBC-Original-Maintainer: Nicolas Mora <babelouest@debian.org>
 Section: libs
 Priority: optional
 Build-Depends: debhelper-compat (= 13),
"""


class TestSavedebdiff(unittest.TestCase):
    # pylint: disable=missing-function-docstring
    """Test savedebdiff."""

    PREFIX = "savedebdiff-"

    def test_derive_filename_from_debdiff(self):
        filename = derive_filename_from_debdiff(unidiff.PatchSet(LIBEVENT_DEBDIFF))
        self.assertEqual(filename, "libevent_2.1.12-stable-5ubuntu1.debdiff")

    def test_debian_changelog_not_found(self):
        empty = unidiff.PatchSet("")
        self.assertRaisesRegex(
            Exception, "No debian/changelog found", derive_filename_from_debdiff, empty
        )

    @unittest.mock.patch("sys.stdin")
    def test_main(self, stdin_mock):
        stdin_mock.read.return_value = LIBEVENT_DEBDIFF
        with tempfile.TemporaryDirectory(prefix=self.PREFIX) as tmpdir:
            main(["--directory", tmpdir])
            self.assertEqual(os.listdir(tmpdir), ["libevent_2.1.12-stable-5ubuntu1.debdiff"])
        stdin_mock.read.assert_called_once_with()

    @unittest.mock.patch("sys.stdin")
    def test_main_no_stdin(self, stdin_mock):
        stdin_mock.read.return_value = ""
        self.assertRaisesRegex(SystemExit, "1", main, [])
        stdin_mock.read.assert_called_once_with()

    @unittest.mock.patch("subprocess.call")
    @unittest.mock.patch("sys.stdin")
    def test_main_open(self, stdin_mock, call_mock):
        stdin_mock.read.return_value = LIBEVENT_DEBDIFF
        expected_filename = "libevent_2.1.12-stable-5ubuntu1.debdiff"
        with tempfile.TemporaryDirectory(prefix=self.PREFIX) as tmpdir:
            main(["--directory", tmpdir, "--open"])
            self.assertEqual(os.listdir(tmpdir), [expected_filename])
            call_mock.assert_called_once_with(
                ["xdg-open", os.path.join(tmpdir, expected_filename)]
            )
        stdin_mock.read.assert_called_once_with()

    def test_save_debdiff(self):
        with tempfile.TemporaryDirectory(prefix=self.PREFIX) as tmpdir:
            filename = os.path.join(tmpdir, "debdiff")
            save_debdiff(filename, "foobar\n", False)
            self.assertEqual(os.listdir(tmpdir), ["debdiff"])
            with open(filename, "r", encoding="utf-8") as written_file:
                self.assertEqual(written_file.read(), "foobar\n")
            stat = os.stat(filename)

            # Test idempotency
            save_debdiff(filename, "foobar\n", False)
            self.assertEqual(os.listdir(tmpdir), ["debdiff"])
            self.assertEqual(os.stat(filename), stat)

            # Test changed content
            self.assertRaisesRegex(SystemExit, "1", save_debdiff, filename, "changed\n", False)

            # Test overwriting content
            save_debdiff(filename, "changed\n", True)
            self.assertEqual(os.listdir(tmpdir), ["debdiff"])
            with open(filename, "r", encoding="utf-8") as written_file:
                self.assertEqual(written_file.read(), "changed\n")
