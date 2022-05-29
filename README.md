Various personal scripts
========================

This repository contains various small personal scripts that have no other place to live. Feel free
to grub through the list.

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
