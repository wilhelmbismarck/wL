"""

# wL
## Exporter

Allows to export `dict` object to a wL file.

### Functions

```
export(obj : dict | list | tuple, config : ExportConfig [optionnal]) # return a str

exports(obj : dict | list | tuple, file : pathlib.Path | str, config : ExportConfig [optionnal]) # create / truncatenate a file
```

### Classes

```
ExportConfig(src : dict) # an export configuration
```

### Others

- `Warning` : 
  - `ConfigWarning`

"""

### Import
from pathlib       import Path
from .exportconfig import ExportConfig
from .exceptions   import ConfigWarning, ExportFileWarning


### Functions
def export(obj : dict | list | tuple, config : ExportConfig | None = None) -> str :
    """
    # Export
    Export a `dict` | `list` | `tuple` obj and return a str. Configurable.
    
    ## Doc
    ### Arguments
    - required : 
      - obj : `dict` | `list` | `tuple` ;
    - optionnal :
      - config : `ExportConfig` ;
    ### Configure
    An `ExportConfig` obj can be used to configure the export.
    
    ExportConfig keys adjust the results.
    
    Here are common keys, and their effect :
    ```
    do_lines    : bool # enables new lines
    do_indent   : bool # enables indentations
    indent_size : int  # adjusts indentations size
    ```
    Consider checking `ExportConfig.config_keys` doc to get a list of all keys.
    Notice that `encoding` does not affect `export()` return, only `exports()`.
    """
    from warnings import warn
    
    if not isinstance(config, ExportConfig):
        config = ExportConfig()
        
    def __stringify(s : str) :
        back  = ''
        for letter in s :
            if   letter in ['\t', '\n', '\v'] : pass
            elif letter in ['\\', '\"', '\''] :
                back += '\\' + letter
            else : back += letter
        return "\"" + back + "\""
    
    def __export(obj, master : str, depth : int, config : ExportConfig) -> str :
        txt = ''
        # Config indent
        if config['do_indent'] and config['do_lines'] :
            indent = ' ' * config['indent_size'] * depth
        else :
            indent = ''
        txt += indent
        # Save data
        if   isinstance(obj, str) :
            txt += f"<{__stringify(master)}={__stringify(obj)}>"
        elif isinstance(obj, dict) :
            if depth > -1 :
                txt += f"<{__stringify(master)}>"
                if config['do_lines'] : txt += '\n'
            for key, item in obj.items() :
                txt += __export(item, str(key), depth + 1, config)
            if config['save_info'] :
                txt += __export('Dictionnary', '__class__', depth + 1, config)
                txt += __export(set(obj.keys()), '__keys__', depth + 1, config)
                txt += __export(set(len(obj)), '__len__', depth + 1, config)
            if depth > -1 :
                txt += indent + "<!>"
                if config['do_lines'] : txt += '\n'
        elif isinstance(obj, set) :
            i = 0
            if depth > -1 :
                txt += f"<{__stringify(master)}>"
                if config['do_lines'] : txt += '\n'
            for value in obj :
                txt += __export(value, str(i), depth + 1, config)
                i += 1
            if config['save_info'] :
                txt += __export('Set', '__class__', depth + 1, config)
                txt += __export(len(obj), '__len__', depth + 1, config)
            if depth > -1 :
                txt += indent + "<!>"
                if config['do_lines'] : txt += '\n'
        elif isinstance(obj, (tuple, list)) :
            if depth > -1 :
                txt += f"<{__stringify(master)}>"
                if config['do_lines'] : txt += '\n'
            key = 0
            for item in obj :
                txt += __export(item, str(key), depth + 1, config)
                key += 1
            if config['save_info'] :
                txt += __export('Iterable', '__class__', depth + 1, config)
                txt += __export(len(obj), '__len__', depth + 1, config)
            if depth > -1 :
                txt += indent + "<!>"
                if config['do_lines'] : txt += '\n'
        else :
            try : 
                if config['save_obj_as_str'] : 
                    txt += f"<{__stringify(master)}=\"{str(obj)}\">"
                else :
                    txt += f"<{__stringify(master)}={str(obj)}>"
            except : 
                warn(f'can not save {obj}', ExportFileWarning)
                pass
        # Config new linew
        if config['do_lines'] : txt += '\n'
        # Safe Return
        return txt
    
    return __export(obj, None, -1, config)
    
def exports(obj : dict | list | tuple, path : str, config : ExportConfig = None) :
    """
    # Exports
    Export a `dict` | `list` | `tuple` obj in file at `path`. Configurable.
    
        ## Doc
    ### Arguments
    - required : 
      - obj  : `dict` | `list` | `tuple` ;
      - path : `str` | `pathlib.Path` ;
    - optionnal :
      - config : `ExportConfig` ;
    ### Configure
    An `ExportConfig` obj can be used to configure the export.
    
    Consider checking both `export()` and `ExportConfig` doc for more details.
    """
    from pathlib import Path
    
    if not isinstance(config, ExportConfig):
        config = ExportConfig()

    txt  = export(obj, config)
    if isinstance(path, Path) :
        file = path.open(mode = 'w', encoding = config['encoding'])
    else                      : 
        file = open(path, mode = 'w', encoding = config['encoding'])
    file.write(txt)
    file.close()
    if not file.name[-3:] == '.wL' :
        Path(file.name).rename(file.name + '.wL')
    return
