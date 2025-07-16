"""

# wL
## Parser

Allows to parse wL.

### Functions

```
load(file : str) # loads wL from a str

loads(file : pathlib.Path | str, encoding : str [optionnal]) # loads wL from a file
```

### Classes

```
LoadConfig(src : dict) # a load configuration
```

### Others

- `Warning` : 
  - `LoadWarning`
- `Exception` : 
  - `ImportError`

"""

### Import
from .exceptions import LoadFileWarning, LoadFileError

def load(wL : str) -> dict :
    """
    # Load
    Load a wL from a string.
    
    ## Doc
    ### Arguments
    - required : 
      - wL : `str` # represents a wL file
      
    Automatically converts accurate `int` | `float` | `bool` | `None`.
    Does not convert back `list` | `tuple`, but index should work, as keys are also converted, plus `dict` objects have a len.
    
    May raise some `LoadFileWarning`, `LoadFileError`.
    """
    # Import
    from warnings import warn
    # EmptyFile Warning
    if len(wL) == 0 :
        warn('wL file is empty', LoadFileWarning)
        return {}
    # RegisterData
    def __data(value):
        if value == 'True' : return True
        elif value == 'False': return False
        elif value == 'None' : return None
        else :
            try : 
                return int(value)
            except : 
                try : 
                    return float(value)
                except :
                    return str(value)
        raise LoadFileError('unable to get data')
    # Recursive Func
    def __load(wL : str, offset : int, depth : int = 0) -> tuple[dict | list, int] :
        # Def
        i   = offset
        run = True
        # Status
        status          = 'none'
        status_start    = -1
        previous_status = (status, 0)
        # Parsing
        name  = ''
        value = ''
        register = {}
        keys     = []
        # SysData
        string = ['\'', '\"']
        system = ['<', '>', '=', '!']
        ignore = [' ', '\n', '\t', '\v', '\r']
        # Loop
        while run :
            if i >= len(wL) :
                raise LoadFileError('wL string index out of range')
            lt = wL[i]
            # Check Letter
            if lt == '\\' :
                if status != 'none' : 
                    i     += 1
                    lt     = wL[i]
                    if lt in system : 
                        raise LoadFileError('wL can not escape sys symbols')
                    value += lt
            elif status in string :
                if lt in system and previous_status[0] == 'name' : 
                    raise LoadFileError(f'wL can not escape sys symbols in name in {previous_status[0]}, even with str')
                if lt == status : 
                    status, status_start = previous_status
                elif not lt in ignore : 
                    value += lt
            elif lt in string :
                previous_status = (status, status_start)
                status_start    = i
                status          = lt
            elif lt in system : 
                previous_status = (status, status_start)
                status_start    = i
                if lt == '<'   :
                    if status != 'none' :
                        raise LoadFileError(f'wL property \"name\" opening on \"{status}\" (at {i}, starting {status_start})')
                    value  = ''
                    name   = ''
                    status = 'name'
                elif lt == '>' :
                    value = __data(value)
                    keys.append(value)
                    if   status == 'name':
                        if value == '' : 
                            raise LoadFileError(f'wL empty name (at {i}, starting {status_start})')
                        register[value], i = __load(wL, i + 1, depth + 1)
                    elif status == 'data':
                        if name == '' : 
                            raise LoadFileError(f'wL empty name (at {i}, starting {status_start})')
                        register[name] = value         
                    else : 
                        raise LoadFileError(f'wL property \"save\" opening on \"{status}\" (at {i}, starting {status_start})')
                    status = 'none'
                elif lt == '=' :
                    if   status == 'name':
                        name  = __data(value)
                        value = ''
                    else : 
                        raise LoadFileError(f'wL property \"set\" opening on \"{status}\" (at {i}, starting {status_start})')
                    status = 'data'
                elif lt == '!' :
                    if status == 'data' : 
                        value += lt
                    elif status == 'name' : 
                        if depth == 0 :
                            raise LoadFileError(f'wL tag \"exit\" on void (at {i}, starting {status_start})')
                        index = wL.find('>', i + 1)
                        if index != -1 :
                            i   = index - 1
                            run = False
                        else : 
                            raise LoadFileError(f'wL tag \"exit\" not closed (at {i}, starting {status_start})')
            elif not lt in (ignore + system) : 
                if status != 'none' :
                    value += lt
            i += 1
            if not run : continue
            if i >= len(wL) :
                if status != 'none' : 
                    raise LoadFileError(f'wL property \"{status}\" not closed (at : end, starting : {status_start})')  
                else : 
                    run = False
        return (register, i)
    
    return __load(wL, 0)[0]

def loads(path : str, encoding : str = "utf-8"):
    """
    # Loads
    Load a wL file.
    
    ## Doc
    ### Arguments
    - required : 
      - path : `str` | `pathlib.Path` ;
    - optionnal :
      - encoding : str # encoding is the same as in builtins `open()` ;
      
    Fore more details, check `load()`.
    """
    from pathlib import Path
    
    if isinstance(path, Path) :
        with path.open(mode = 'r', encoding = encoding) as file : 
            ret = file.read()
    else                      : 
        with open(path, mode = 'r', encoding = encoding) as file :
            ret = file.read()
    
    return load(ret)
