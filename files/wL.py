class wL:
    """wL / File class"""
    
    version    : str   = '00113'
    wL_version : str   = 'v1.1'
    systemSymb : tuple = ('<', '>', '=', '!')
    
    def __init__(self):
        """wL / New object."""
        self.dict : dict = {}
        
    def pack(self, open = 'todo', master : str = '', tab : str = '    ', depth : int = 0) -> str:
        """wL / Pack a wL object and return it as a txt str."""
        txt : str = ''
        if open == 'todo'           : dic = self.dict
        else                        : dic = open
        if isinstance(dic, list) or isinstance(dic, dict) :
            if depth > 0                 : txt += tab * (depth -1) + '<' + master + '>' + '\n'
            if   isinstance(dic, list)   : # notice than a wL should not contain lists, but dicts with str numbers as keys.
                for i in range(len(dic)) : txt += self.pack(open = dic[i], master = str(i), tab = tab, depth = depth + 1)
            elif isinstance(dic, dict)   :
                for key in dic.keys()    : txt += self.pack(open = dic[key], master = self.__str(key), tab = tab, depth = depth + 1)
            if depth > 0                 : txt += tab * (depth -1) + '<!>' + '\n'
        else                             : txt += tab * (depth -1) + '<' + master + '=' +  self.__str(dic) + '>' + '\n'
        return txt
                    
    def unpack(self, file : str, forceErrors : bool = True) -> dict:
        """wl / Open wL file in self. Overwritte former dict. Also return wL dict.\nFile needed, plus an additional parameter to ignore passive errors."""
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
                    if letter in self.systemSymb and forceErrors : raise ValueError('at {idx}, name contain system symbols (\"<\", \">\", \"=\", \"!\") [wL:08].')
                    else                                         : name += letter
                elif wRNm == 'data'                              : data += letter
            else     : # System & Raw Gestion
                if letter in ['\'', '\"']:
                    if   wRNm == 'name' and len(name) > 0 : raise ValueError(f'at {idx}, can\'t use multiple str [wL:06a].')
                    elif wRNm == 'data' and len(data) > 0 : raise ValueError(f'at {idx}, can\'t use multiple str [wL:06b].')
                    isStr = letter
                elif letter in ['\x20', ' ', '\n', '\r', '\t', '\v']: name = name #whitespace     
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
                            newD = self.__save(newD, path, value = {})
                        else             :
                            if len(path) == 0: raise ValueError(f'at {idx}, \'!\' is closing void [wL:02].')
                            path.pop()
                    else            : newD = self.__save(newD, path + [name], data)
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
        self.dict = newD
        return newD
                
    def __save(self, dic : dict, path : list, value = 'null') -> dict:
        """wL / Functions / In a dict 'dic', following a list 'path of keys', edit last key with value, and return dic."""
        copyDic = dic # copy of dic
        # Iterate all except last key
        for key in path[:-1]:
            if key not in copyDic : copyDic[key] = {}  # Create a new dict if path is not valid
            copyDic = copyDic[key]
        # Edit last key
        if path[-1] in copyDic.keys(): raise ValueError('file contain duplicated data [wL:07]')
        copyDic[path[-1]] = value
        return dic
    
    def __str(self, data, allowSystem : bool = True) -> str:
        """wL / Functions / Convert data to str and stringify if contain system symbols."""
        build = str(data)
        back  = ''
        for letter in build:
            if letter in ['\\', '\"'] :
                if allowSystem : back += '\\' + letter
            else : back += letter
        if allowSystem : return "\"" + back + "\""
        else : return back
        
    def exportXML(self, open = 'todo', master = 'xml', tab : str = '    ', depth : int = 0) -> str:
        """wL / Pack a wL object as an XML file and return it as a txt str."""
        txt : str = ''
        if open == 'todo'           : dic = self.dict
        else                        : dic = open
        if isinstance(dic, list) or isinstance(dic, dict) :
            if depth >= 0                : txt += tab * depth + '<' + master + '>' + '\n'
            if depth == 0                : txt += tab * 1 + f'<source>wL:v2:py-{self.version}:</source>\n'
            if   isinstance(dic, list)   : 
                for i in range(len(dic)) : txt += self.exportXML(open = dic[i], master = str(i), tab = tab, depth = depth + 1)
            elif isinstance(dic, dict)   :
                for key in dic.keys()    : txt += self.exportXML(open = dic[key], master = self.__str(key, False), tab = tab, depth = depth + 1)
            if depth >= 0                : txt += tab * depth + '</' + master + '>' + '\n'
        else                             : txt += tab * depth + '<' + master + '>' + self.__str(dic, False) + '</' + master + '>' + '\n'
        return txt
    
    def get(self) -> dict:
        """wL / Get wL dict."""
        return self.dict 
    
def wL_info() -> str:
    """wL / Print informations about wL. Return current version id."""
    print(f"""
############### wL ###############
          
 [wilhelm43, version {wL().version}, CC-BY-SA]
          
wL is a "markup" "metalanguage" designed to store arbitrary data in a format that is both human-readable and machine-readable.
The design goals of wL emphasize elementary simplicity, generality, stability, and usability across all programming language.
          
##################################
          """)
    return wL().version
