# imgprepper

`imgprepper` is a Python script that will take your list of image files, then resize, rename and optimise their size, saving them in a directory of your choice.

Design your resize options as individual presets in a YAML file. Works with JPEG and PNG files and returns them in the same format.

It is built using Pillow and ImageOptim-CLI.

## Requirements

* macOS &mdash; tested on 10.14.3. Necessary because of ImageOptim being Mac only.
* Python 3.7+ &mdash; untested on below, not compatible with Python 2)
* [Pillow for Python](https://pillow.readthedocs.io/en/stable/) &mdash; image processing library
* [`ImageOptim for Mac`](https://imageoptim.com/mac) &mdash; the free open-source GUI
* [`imageoptim-cli`](https://github.com/JamieMason/ImageOptim-CLI) &mdash; installed as a regular command line utility for your system

## To install

1. Download `imgprepper.py`
2. If not already installed, install `imageoptim-cli` ([see installation instructions](https://github.com/JamieMason/ImageOptim-CLI#installation)):

```
brew install imageoptim-cli
```

## To use

1. Create a text file using YAML structure (e.g. `presets.yml`) in your text editor, according to the following format:

```yaml
presets:
  - action: resize
    width: 1280
    nameFormat: "{name}_large.{ext}"
    directory: /Users/me/dest

file_paths: |
  /Users/me/source/file.jpg
```

* Create as many presets as needed. At the moment, the script will run all of them.
* **Remember**: indent the file paths with two spaces, in order to have correct YAML formatting.

2. Run the script:

```
python imgprepper.py presets.yml
```

3. In your terminal, you'll be given a running log of the resize process. ImageOptim will also present its results at the end.

```
Directory out: /Users/me/dest/
    file_large.jpg | Dimensions: 1280 x 853 | Resize: 1.661 s

i Running ImageOptim...
✓ /Users/me/dest/file_large.jpg was: 68.2kB now: 68.2kB saving: 0B (0.00%)
```

---
## Documentation

### YAML presets file
#### Two main keys

| Key | Type | Default | Description |
|-|-|-|-|
| `presets` | List of items | | Each format is its own list. At the moment, the script will run all of them.
| `file_paths` | String | | A string containing file paths, on their own line. Can be JPEG and/or PNG.

#### Inside each item in `presets`

All are required, except where marked optional.

| Key | Type | Default | Description |
|-|-|-|-|
| `action` | String | `resize` | The type of action to perform. At the moment, only `resize` is supported.
| `width` | Integer | | The desired width to resize to. The height is determined proportionally and can't be specified.
| `nameFormat` | String | | How to name the destination file. Must use `{name}` and `{ext}`, where name is the original name of the input file.
| `options` | List | | *Optional*: Options for saving and compressing.

#### Inside `options`

Refer to [Pillow documentation for more details](https://pillow.readthedocs.io/en/stable/) on what the result of these values are.

| Key | Type | Default | Description |
|-|-|-|-|
| `quality` | Integer | 85 | JPEG quality.
| `optimize` | Boolean | True | Optimize JPEG size.
| `resample` | String | `LANCZOS` | Type of resizing algorithm. Lanczos is the 'best' for reduction.

---

## Development to-do

* Offer an option to just use standard ImageOptim.app for MacOS.
* Investigate the actual JPEG compression libraries themselves and consider including them manually, bypassing ImageOptim and ImageOptim-CLI. This could then enable the creation of a standalone binary using PyInstaller.
* Offer an option to enable/disable certain presets, either by command line or a 'disable' key in YAML.
