"""
# wL

wL is a "markup" "metalanguage" designed to store arbitrary data in a format that is both human-readable and machine-readable.
The design goals of wL emphasize elementary simplicity, generality, stability, and usability across all programming language.

- wL by       : wilhelm43 ;
- lib version : 1.3.3 ;
- supports wL : 1.0, 1.1 ;



Sub packages :


- `exporter`, which allows to :
  - export to str (`export`) ;
  - export to file (`exports`) ;

- `parser`, which allows to :
  - parse from str (`load`) ;
  - parse from file (`loads`) ;
  

Consider checking each sub packages documentation.
"""

supports : tuple[str] = ("1.1", "1.0")
"""Supported wL versions by `parser`. The first is always the one used by `exporter`."""
version  : str        = "1.3.3"
"""wL package version"""
