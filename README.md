# wL

**wL** is a *markup metalanguage* designed to store arbitrary data in a format that is both human-readable and machine-readable.

The design goals of wL emphasize elementary simplicity, generality, stability, and usability across all programming language.
Plus, wL format does not contain no data specialisation or typing, for a linear read.

## Python module

wL's python module contain two files, `wL.py` and `wL-demo.py`. `wl.py` contain module, functions and wL class ; while `wL-demo.py` contain a small demo of wL pack / unpack.

### Module

Module contain all scripts required for your wL use.

Start by importing wL using 
```python
import wL as wLm # example alternate name, module should not be opened with "wL" as name
```

Importing files
```python
mywL = wLm.wK()
mywL.unpack(file = '…')
```

Exporting files
```python
file = open("file.txt", "w") # or .wL
file.write(mywL.pack())
file.close()
```

### Demo

Demo [`wL-demo.py`] pack and unpack an example wL dict.

## Licence

wL is an open-source format defined by this conventions : 
wL python module is CC-BY-SA (latest).