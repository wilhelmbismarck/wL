# wL

<img width="160" src="https://raw.githubusercontent.com/wilhelmbismarck/wL/8fb954343c74cfc783c3b266d3dc52ad0698ddd2/wL.svg">

**wL** is a *markup metalanguage* designed to store arbitrary data in a format that is both human-readable and machine-readable.

The design goals of wL emphasize elementary simplicity, generality, stability, and usability across all programming language.
Plus, wL format does not contain no data specialisation or typing, for a linear read.

Consider checking the [GitHub rep](https://github.com/wilhelmbismarck/wL/) to get a full documentation.

## Packages

`wLpylib` itself does not coutain any function, class.
You should import either `wLpylib.exporter` or `wLpylib.parser`.

## Doc

### Exporter

Coutains two functions to export to a str, or a file (supports pathlib.Path). Additionally coutains a configure class.

```python
from wLpylib.exporter import export, exports, ExportConfig

export(obj, config)        # export obj to a str following rules in config
exports(obj, path, config) # export obj to bounded file following rules in config

ExportConfig(src) # configuration for both export functions
```

### Parser

Coutains two functions to parse wL from a str, or a file (supports pathlib.Path).

```python
from wLpylib.exporter import export, exports

load(obj, config)        # parse wL from a str
loads(obj, path, config) # parse wL from a file
```