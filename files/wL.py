## About wL
## ========
##
## wL is a "markup" "metalanguage" designed to store arbitrary data in a format that is both human-readable and machine-readable.
## The design goals of wL emphasize elementary simplicity, generality, stability, and usability across all programming language.
##
## - wL by       : wilhelm43
## - lib version : 1.2.0
## - supports wL : 1.0, 1.1
##
  
__sysSymb : tuple = ("=", "<", ">", "!")
__ver_wL  : tuple = ("1.0", "1.1")
__ver_lib : str   = "1.2.0"
              
def export_wL(obj : dict, master : str = '', tab : str = '    ', depth : int = 0) -> str:
        """wL / Pack a wL object and return it as a txt str."""
        txt : str  = ''
        dic : dict = obj
        if isinstance(dic, list) or isinstance(dic, dict) :
            if depth > 0                 : txt += tab * (depth -1) + '<' + master + '>' + '\n'
            if   isinstance(dic, list)   : # notice than a wL should not contain lists, but dicts with str numbers as keys.
                for i in range(len(dic)) : txt += export_wL(obj = dic[i], master = str(i), tab = tab, depth = depth + 1)
            elif isinstance(dic, dict)   :
                for key in dic.keys()    : txt += export_wL(obj = dic[key], master = __wLstr(key), tab = tab, depth = depth + 1)
            if depth > 0                 : txt += tab * (depth -1) + '<!>' + '\n'
        else                             : txt += tab * (depth -1) + '<' + master + '=' +  __wLstr(dic) + '>' + '\n'
        return txt
                    
def import_wL(file : str, fE : bool = True) -> dict:
        """wl / Open wL file in self. Overwritte former dict. Also return wL dict.
        \nFile needed, plus an additional parameter to ignore passive errors."""
        # Start errors
        if len(file) == 0: raise ValueError('file is blank [wL:00a].')
        # Definitions
        path  = []
        newD  = {}
        wRNm  = ''
        name, data = ('', '')
        isStr = None
        # Opening file
        idx = 0
        while idx < (len(file)):
            letter = file[idx]
            if   letter == '\\' : # Backslash gestion
                idx += 1
                if   wRNm == 'name' : name += file[idx]
                elif wRNm == 'data' : data += file[idx]
            elif not isStr is None  : # STR Gestion
                if letter in isStr  : isStr = None
                elif wRNm == 'name' : 
                    if letter in __sysSymb and fE : raise ValueError('at {idx}, name contain system symbols (\"<\", \">\", \"=\", \"!\") [wL:08].')
                    else                          : name += letter
                elif wRNm == 'data'               : data += letter
            else     : # System & Raw Gestion
                if letter in ['\'', '\"']:
                    if   wRNm == 'name' and len(name) > 0 : raise ValueError(f'at {idx}, can\'t use multiple str [wL:06a].')
                    elif wRNm == 'data' and len(data) > 0 : raise ValueError(f'at {idx}, can\'t use multiple str [wL:06b].')
                    isStr = letter
                elif letter in ['\x20', ' ', '\n', '\r', '\t', '\v']: pass 
                elif letter == '<':
                    if wRNm in ['name', 'data']: raise ValueError(f'at {idx}, \'<\' is alone / dupe [error{wRNm}] [wL:01a].')
                    wRNm = 'name'
                    name = ''
                    data = None
                elif letter == '>':
                    if wRNm == ''    : raise ValueError(f'at {idx}, \'>\' is alone [wL:01b].')
                    if len(name) == 0: raise ValueError(f'at {idx}, name is empty [wL:03a].')
                    wRNm = ''
                    if data is None :
                        if len(name) == 0 : name = 'null'
                        if name[0] != '!' :
                            path.append(name)
                            newD = __wLdictSave(newD, path, value = {})
                        else             :
                            if len(path) == 0: raise ValueError(f'at {idx}, \'!\' is closing void [wL:02].')
                            path.pop()
                    else            : newD = __wLdictSave(newD, path + [name], data)
                elif letter == '=':
                    if wRNm in ['', 'data']: raise ValueError(f'at {idx}, \'=\' is alone / dupe [error{wRNm}] [wL:01c].')
                    if len(name) == 0      : raise ValueError(f'at {idx}, name is empty [wL:03b].')
                    wRNm = 'data'
                    data = ''
                elif wRNm == 'name' : name += letter
                elif wRNm == 'data' : data += letter
            idx += 1
            # While reloop
        # EnfOfFile Errors
        if len(newD.keys()) == 0 : raise EOFError('file does not contain data [wL:00b].')
        if not wRNm == ''        : raise EOFError(f'at end, {wRNm} is not closed [wL:04].')
        if len(path) > 0         : raise EOFError('at end, path is not closed [wL:05].')
        # Finitions
        return newD
                
def __wLdictSave(dic : dict, path : list, value = 'null') -> dict:
        """wL / Functions / In a dict, following a list 'path of keys', edit last key with value, and return dic."""
        copyDic = dic # copy of dic
        # Iterate all except last key
        for key in path[:-1]:
            if key not in copyDic : copyDic[key] = {}  # Create a new dict if path is not valid
            copyDic = copyDic[key]
        # Edit last key
        if path[-1] in copyDic.keys(): raise ValueError('file contain duplicated data [wL:07]')
        copyDic[path[-1]] = value
        return dic
    
def __wLstr(data, allowSystem : bool = True) -> str:
        """wL / Functions / Convert data to str and stringify if contain system symbols."""
        build = str(data)
        back  = ''
        for letter in build:
            if letter in ['\\', '\"'] :
                if allowSystem : back += '\\' + letter
            else : back += letter
        if allowSystem : return "\"" + back + "\""
        else : return back
        
def export_XML(obj : dict, master = 'xml', tab : str = '    ', depth : int = 0) -> str:
        """wL / Pack a wL object as an XML file and return it as a txt str."""
        txt : str  = ''
        dic : dict = obj
        if isinstance(dic, list) or isinstance(dic, dict) :
            if depth >= 0                : txt += tab * depth + '<' + master + '>' + '\n'
            if   isinstance(dic, list)   : 
                for i in range(len(dic)) : txt += export_XML(obj = dic[i], master = str(i), tab = tab, depth = depth + 1)
            elif isinstance(dic, dict)   :
                for key in dic.keys()    : txt += export_XML(obj = dic[key], master = __wLstr(key, False), tab = tab, depth = depth + 1)
            if depth >= 0                : txt += tab * depth + '</' + master + '>' + '\n'
        else                             : txt += tab * depth + '<' + master + '>' + __wLstr(dic, False) + '</' + master + '>' + '\n'
        return txt
