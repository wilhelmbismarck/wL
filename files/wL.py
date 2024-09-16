class wL:
    """wL / File class"""
    
    version : str = '00110'
    
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
                for key in dic.keys()    : txt += self.pack(open = dic[key], master = str(key), tab = tab, depth = depth + 1)
            if depth > 0                 : txt += tab * (depth -1) + '<!>' + '\n'
        else                             : txt += tab * (depth -1) + '<' + master + '=\"' + str(dic) + '\">' + '\n'
        return txt
                    
    def unpack(self, file : str) -> dict:
        """wl / Open wL file in self. Overwritte former dict. Also return wL dict."""
        # Definitions
        path  = []
        newD  = {}
        wRNm  = ''
        name, data = ('', '')
        isStr = False
        # Opening file
        for idx in range(len(file)):
            letter = file[idx]
            if isStr : # STR Gestion
                if letter in ['\'', '\"']: isStr = False
                elif wRNm == 'name' : name += letter
                elif wRNm == 'data' : data += letter
            else     : # System & Raw Gestion
                if letter in ['\'', '\"']:
                    if   wRNm == 'name' and len(name) > 0 : raise ValueError(f'at {idx}, can\'t use multiple str [wL:06a].')
                    elif wRNm == 'data' and len(data) > 0 : raise ValueError(f'at {idx}, can\'t use multiple str [wL:06b].')
                    isStr = True
                elif letter in [' ', ' ', '\n']: name = name #whitespace     
                elif letter == '<':
                    if wRNm in ['name', 'data']: raise ValueError(f'at {idx}, \'<\' is alone / dupe [error{wRNm}] [wL:01a].')
                    wRNm = 'name'
                    name = ''
                    data = None
                elif letter == '>':
                    if wRNm == ''    : raise ValueError(f'at {idx}, \'>\' is alone. [wL:01b]')
                    if len(name) == 0: raise ValueError(f'at {idx}, name is empty. [wL:03a]')
                    wRNm = ''
                    if data is None :
                        if len(name) == 0 : name = 'null'
                        if name[0] != '!' :
                            path.append(name)
                            newD = self.__save(newD, path, value = {})
                        else             :
                            if len(path) == 0: raise ValueError(f'at {idx}, \'!\' is closing void. [wL:02]')
                            path.pop()
                    else            : newD = self.__save(newD, path + [name], data)
                elif letter == '=':
                    if wRNm in ['', 'data']: raise ValueError(f'at {idx}, \'=\' is alone / dupe [error{wRNm}]. [wL:01c]')
                    if len(name) == 0      : raise ValueError(f'at {idx}, name is empty. [wL:03b]')
                    wRNm = 'data'
                    data = ''
                elif wRNm == 'name' : name += letter
                elif wRNm == 'data' : data += letter
        # EnfOfFile Errors
        if not wRNm == '' : raise EOFError(f'at end, {wRNm} is not closed.  [wL:04]')
        if len(path) > 0  : raise EOFError('at end, path is not closed.  [wL:05]')
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
        copyDic[path[-1]] = value
        return dic
        
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
                for key in dic.keys()    : txt += self.exportXML(open = dic[key], master = str(key), tab = tab, depth = depth + 1)
            if depth >= 0                : txt += tab * depth + '</' + master + '>' + '\n'
        else                             : txt += tab * depth + '<' + master + '>' + str(dic) + '</' + master + '>' + '\n'
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
