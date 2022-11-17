Various personal scripts
========================

This repository contains various small personal scripts that have no other place to live. Feel free
to grub through the list.

bzr2git
-------

Convert a bzr repository to git. It takes a bzr clone URL or a local bzr
repository and a git remote URL. The converted git repository is checked to have
the same content and that the author/committer names and emails are correct
(using `userlint`).

Example call:

```sh
bzr2git lp:jasper-initramfs git+ssh://git.launchpad.net/~ubuntu-dev/jasper-initramfs/+git/main
```

In case the author/committer names and emails needs to be corrected:

```sh
cat > whoopsie.mailmap <<EOF
Evan Dandrea <evan.dandrea@canonical.com> Tarmac <>
EOF
bzr2git -m whoopsie.mailmap lp:whoopsie git+ssh://git.launchpad.net/~ubuntu-core-dev/whoopsie/+git/main
```

As of 2022 some converted git repositories had different content compared to the
original bzr repositories due to not correctly moved files. You can fix this by
following step:

1. Figure out which commit is broken and check out this commit.
2. Commit a fix-up with the commit message "Fix history".
3. Create `fix.py` containing a Python commit callback to record the changes of
   the fix-up commit:
   ```python
   if commit.message.startswith(b"Fix history"):
       print(
           f"\n### {commit.message.decode()!r}. parents = {commit.parents!r} ###\n"
           f'if commit.message.startswith(b"TODO"):\n'
           f'    print(f"### Fix commit {"{"}commit.message.decode()!r{"}"} ###")\n'
           f"    commit.file_changes += ["
       )
       for fc in commit.file_changes:
           fc_repr = f"        FileChange({fc.type!r}, {fc.filename!r}, {fc.blob_id!r}, {fc.mode!r}),"
           print(fc_repr.replace(chr(39), '"'))
       print("    ]")
   ```
4. Run `git-filter-repo` in the git repository with this `fix.py` as commit
   callback:
   ```sh
   git-filter-repo --force --replace-refs=delete-no-add --commit-callback fix.py
   ```
   It should print a Python snippet with the changes from the fix-up commit.
5. Copy the Python snippet into `fix.py` and replace `TODO` by the commit
   message from the commit that you want to fix.
6. Run `bzr2git` again with `--commit-callback fix.py` added.

copy-mtime
----------

Copy the modification time from one file to another.

Example call:

```
copy-mtime source_file target_file
```

generate-gallery
----------------

Generate picture gallery using fgallery (configured by YAML file).

Example YAML configuration `example.yaml`:

```YAML
output_dir: fgallery
temp_dir: fgallery/source
galleries:
  - name: example_gallery
    source: pictures/2019/example/*.jpg
```

Running `generate-gallery -c example.yaml` would create `fgallery/example_gallery` using the
pictures from `pictures/2019/example/*.jpg`. The paths can be absolute or relative to the
configuration file.

git-archive
-----------

Generate a Debian source package from a git repository using `git archive`.
The script reads `debian/changelog` to determine the source package name and
upstream version. It will write the Debian source package to
`../${source}_${upstream_version}.orig.tar.xz`. The script takes one parameter
to specify which tree-ish should be archived (defaults to `HEAD`). Example call:

```
git-archive main
```

savedebdiff
-----------

Save the debdiff output as `<source>_<version>.debdiff`. Pipe the debdiff output
to `savedebdiff`. The diff must contain new `debian/changelog` entry.

Example call:

```
debdiff --auto-ver-sort libevent_*.dsc | savediff --open
```

userlint
--------

Check git authors and commits for correct names and email addresses.

Example call:

```
userlint
```

Example successful output:

```
userlint INFO: Checked 25 commits, found 2 valid and no invalid entries.
```

Example for an invalid email address:

```
userlint WARNING: Checked 2 commits, found 1 valid and 1 invalid entries:
Benjamin Drung <bdrung@localhost>
userlint INFO: Suggested mailmap:
Benjamin Drung <bdrung@ubuntu.com> Benjamin Drung <bdrung@localhost>
```

wallpaper-slideshow
-------------------

Create a GNOME wallpaper slideshow.

Example call:

```
wallpaper-slideshow -n "Vacation 2019" ~/Pictures/2019_Vacation"
```

This would create a slideshow named `Vacation 2019` using all images from the
directory `~/Pictures/2019_Vacation`.

webcam-capture
--------------

`webcam-capture` uses FFmpeg to capture the output of Cam Link 4K device (Audio and Video).

Example call:

```
webcam-capture
```
