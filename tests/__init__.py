# Copyright (C) 2017-2021, Benjamin Drung <benjamin.drung@ionos.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""Helper functions for testing."""

import inspect
import os
import unittest


def get_source_files():
    """Return a list of sources files/directories (to check with flake8/pylint)."""
    scripts = [
        "copy-mtime",
        "dpkg-which",
        "generate-gallery",
        "savedebdiff",
        "schroot-wrapper",
        "userlint",
        "wallpaper-slideshow",
    ]
    modules = ["tests"]
    py_files = []

    files = []
    for code_file in scripts + modules + py_files:
        is_script = code_file in scripts
        if not os.path.exists(code_file):  # pragma: no cover
            # The alternative path is needed for Debian's pybuild
            alternative = os.path.join(os.environ.get("OLDPWD", ""), code_file)
            code_file = alternative if os.path.exists(alternative) else code_file
        if is_script:
            with open(code_file, "rb") as script_file:
                shebang = script_file.readline().decode("utf-8")
            if "python" in shebang:
                files.append(code_file)
        else:
            files.append(code_file)
    return files


def unittest_verbosity():
    """
    Return the verbosity setting of the currently running unittest.

    If no test is running, return 0.
    """
    frame = inspect.currentframe()
    while frame:
        self = frame.f_locals.get("self")
        if isinstance(self, unittest.TestProgram):
            return self.verbosity
        frame = frame.f_back
    return 0  # pragma: no cover
