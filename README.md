# wL

<img src="wL.svg" align="right">

**wL** is a *markup metalanguage* designed to store arbitrary data in a format that is both human-readable and machine-readable.

The design goals of wL emphasize elementary simplicity, generality, stability, and usability across all programming language.
Plus, wL format does not contain no data specialisation or typing, for a linear read.

## Python module

> "lib" refer to `wL.py`

### Importing lib

Importing with `pip` :
```bash
pip install wLpylib
```
```zsh
python3 -m pip install wLpylib
```
```python
import wLpylib as wL
import wLpylib.parser   as wL_parse
import wLpylib.exporter as wL_export
```

### Functions

The doc uses pathlib.Path as some functions support it. *Its use is not required*.
```python
from pathlib import Path
```

Parse wL from a file : 
```python
wL_parse.loads('file.wL')
wL_parse.loads(Path('file.wL'))
# Open a file and parse its wL
# - ".wL" is required at the end of the file path
wL_parse.loads('file.wL', encoding = "utf-8")
# Open a file following an enconding rules and parse its wL
```
Parse wL from a string : 
```python
wL_parse.load('<wL><!>') -> {'wL' : {}}
# parse a wL from a str object
```

Export an object (if possible) to a wL file
```python
obj : dict | list | tuple = ...
wL_export.exports(obj, path = 'file.wL')
wL_export.exports(obj, path = Path('file.wL'))
```
Export an object (if possible) to a wL str
```python
obj : dict | list | tuple = ...
wL_export.export(obj)
```
Configure export : 
```python
myConfig = wL_export.ExportConfig(src = {'encoding' : 'utf-8', …})
wL_export.export(obj, config = myConfig)
wL_export.exports(obj, path = 'file.wL', config = myConfig)
wL_export.exports(obj, path = Path('file.wL'), config = myConfig)

myConfig = wL_export.ExportConfig(src = \
{'encoding' : 'utf-8',     # only used by exports(), represents the file.write() encoding
 'save_info' : False,      # not used yet
 'save_obj_as_str' : True, # try to saves every object with str()
 'do_lines' : True,        # enables new lines
 'do_indent' : True,       # enables indentations, requires enabling "do_lines"
 'indent_size' : 4         # adjust indent size, requires enabling "do_indent"
})
```

## License

wL is an open-source format defined by [this conventions](https://wilhelm43.notion.site/wL-027498635f0745c586c4beaf2e36f0a1). 

wL python package license is `CC-BY-SA` (`4.0`).

----
