# imgprepper

`imgprepper` is a Python script that will take your list of image files, then resize, rename and optimise their size, saving them in a directory of your choice.

Design your resize options in a preset in `job.py`.

It is built using Pillow and ImageOptim-CLI.

### Requirements

* Python 3.7+ &mdash; untested on below, not compatible with Python 2)
* [`ImageOptim for Mac`](https://imageoptim.com/mac) &mdash; the free open-source GUI
* [`imageoptim-cli`](https://github.com/JamieMason/ImageOptim-CLI) &mdash; installed as a regular command line utility for your system

### To install

1. Download `imgprepper.py` and `job.py`
2. If not already installed, install `imageoptim-cli` ([see installation instructions](https://github.com/JamieMason/ImageOptim-CLI#installation)):

```
brew install imageoptim-cli
```

### To use

1. Edit your `job.py` file according to the following format. At the moment, only `resize` is accepted.

```python
TARGET_PRESETS = [
    {
        'action': 'resize',
        'width': 1280,
        'nameFormat': '{name}_large.{ext}',
        'directory': '/Users/me/dest'
    }
]

LIST_OF_FILE_PATHS = """

/Users/me/source/file.jpg

"""
```

2. Run the main script: `imgprepper.py`

```
python imgprepper.py
```

3. In your terminal, you'll be given a running log of the resize process. ImageOptim will also present its results at the end.

```
Directory out: /Users/me/dest/
    file_large.jpg | Dimensions: 1280 x 853 | Resize: 1.661 s

i Running ImageOptim...
✓ /Users/me/dest/file_large.jpg was: 68.2kB now: 68.2kB saving: 0B (0.00%)
```

---

### Development to-do

* Offer an option to just use standard ImageOptim.app for MacOS.
