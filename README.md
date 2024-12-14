# wL

**wL** is a *markup metalanguage* designed to store arbitrary data in a format that is both human-readable and machine-readable.

The design goals of wL emphasize elementary simplicity, generality, stability, and usability across all programming language.
Plus, wL format does not contain no data specialisation or typing, for a linear read.

## Python module

> "lib" refer to `wL.py`

### Importing lib
- by downloading lib (*add the lib in your script's repository*)
```python
import wL as wLlib
```
- from pip
```bash
pip install wLpylib
```
```zsh
python3 -m pip install wLpylib
```
```python
import wLpylib as wLlib
```

### Functions

Open a wL file
```python
wLlib.import_wL(open("file.wL"))
```
Export a `dict` as a wL file
```python
wLlib.export_wL(any_dict)
```
Export a `dict` as a XML file
```python
wLlib.export_XML(any_dict)
```

## License

wL is an open-source format defined by [this conventions](https://wilhelm43.notion.site/wL-027498635f0745c586c4beaf2e36f0a1). 

wL python module license is `CC-BY-SA` (`4.0`).

----
