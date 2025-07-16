from warnings   import warn
from .exceptions import ConfigWarning

class ExportConfig :
    """
    # ExportConfig
    Represent a configuration to export file.
    
    Full doc by hovering `ExportConfig()`, or running `ExportConfig.doc()`
    """
    
    config_keys : dict[str, tuple[type, object]] = \
    {'save_info '      : (bool, False, 'saving extra data for some types'),
     'save_obj_as_str' : (bool, True, 'saving every obj in a string'),
     'do_lines'        : (bool, True, 'new lines'),
     'do_indent'       : (bool, True, 'indentation'),
     'indent_size'     : (int, 4, 'indentation size', (0, 16)),
     'encoding'        : (str, "utf-8", 'string encoding', ("utf-8", ""))
    }
    """
    # ExportConfig keys
    All keys expected in a `ExportConfig`.
        
    - Use ExportConfig.doc() for more a list.
    - Use ExportConfig.doc(key) to get a key documentation.
    """
    
    def __init__(self, src : dict = {}) :
        """
        # ExportConfig init
        Create a new ExportConfig object.
       
        ## Doc
        ### Arguments
        - optionnal :
          - src,
            a dic coutaining export instructions ;
        ### How to use
        Leave `src` empty to get the default config.
        
        If you need a customised config, use `src` or setter `config[key] = value`. 
        The `src` dict coutains should coutains at least one key from `ExportConfig.config_keys` (read its doc).
        """
        self.config  : dict = {}
        self.version : str  = '1.0'
        if src != {} : self.__from_dict(src)
        else         : self.__default()
         
    def __set_key(self, configkey : str, value) :
        """Set `configkey` to `value` with check."""
        if configkey in ExportConfig.config_keys :
            if not configkey in self.config :
                self.config[configkey] = None
            item = self.config_keys[configkey]
            self.config[configkey] = value
            if len(item) > 3 :
                # Check Type
                if not isinstance(item[3], tuple)  :
                    raise SystemError('ExportConfig.__from_dict.check_key.check_range.int RANGE is not a tuple')
                # - int
                if item[0] == int : 
                    
                    if not len(item[3]) == 2           :
                        raise SystemError(f'ExportConfig.__from_dict.check_key.check_range.int RANGE invalid len (expected 2, got {len(item[3])})')
                    if not isinstance(item[3][0], int) :
                        raise SystemError('ExportConfig.__from_dict.check_key.check_range.int RANGE[0] invalid type (expecting int)')
                    if not isinstance(item[3][1], int) :
                        raise SystemError('ExportConfig.__from_dict.check_key.check_range.int RANGE[1] invalid type (expecting int)')
                    if not isinstance(value, int)      :
                        value = item[1]
                        return
                    rg_min, rg_max = min(item[3]), max(min(item[3]))
                    # Check Range
                    if self.config[configkey] < rg_min   :
                        self.config[configkey] = rg_min
                        warn(f"wl.ExportConfig(src), src[{configkey}] : out of range [{rg_min} ; {rg_max}]", ConfigWarning)
                    elif self.config[configkey] > rg_max :
                        self.config[configkey] = rg_max
                        warn(f"wl.ExportConfig(src), src[{configkey}] : out of range [{rg_min} ; {rg_max}]", ConfigWarning)
                # - str
                elif item[0] == str : 
                    if not value in item[3] : 
                        warn(f"wl.ExportConfig(src), src[{configkey}] : \"{value}\" is not a possible value", ConfigWarning)
                        self.config[configkey] = item[1]
                # End Check Type
            return
            # End
        raise KeyError(f'key {configkey} not a config key')        
          
    def __from_dict(self, src : dict) -> tuple[int, int] :
        """
        Merge `src` into ExportConfig obj.
        Return marged, passed keys count.
        """
        count_passed = 0
        count_merged = 0
        view = ExportConfig.config_keys
        for key, item in view.items() :
            if key in src : 
                # Check key
                if not isinstance(item[0], type)     : pass
                elif   isinstance(src[key], item[0]) :
                    # Check range for int
                    self.__set_key(key, src[key])
                    # Count
                    count_merged += 1
                    continue
                else : 
                    warn(f"wl.ExportConfig(src), src[{key}] : unexpected type {type(src[key])}, expected {item}", ConfigWarning)
            # Count
            count_passed += 1
        return (count_merged, count_passed)
    
    def __default(self) -> None :
        """Create default config"""
        view = ExportConfig.config_keys
        for key, item in view.items() :
            if not isinstance(item, tuple) :
                raise SystemError(f'ExportConfig.__default RANGE[1] key "{key}" value is not a tuple.')
            if len(item) < 3 :
                raise SystemError(f'ExportConfig.__default RANGE[1] key "{key}" tuple is missing {3 - len(item)} value.')
            self.config[key] = item[1]
        return
            
    def __setitem__(self, configkey : str, value) :
        """Set [if existing] `configkey` to `value`."""
        self.__set_key(configkey, value)
        
    def __getitem__(self, configkey : str) :
        """Get [if existing] `configkey`."""
        if configkey in self.config :
            return self.config[configkey]
        if configkey in self.config_keys :
            return self.config_keys[configkey][1]
        raise KeyError(f'key {configkey} not a config key')      
    
    @staticmethod
    def doc(configkey : str = None) :
        """
        # ExportConfig doc
        Print a key documentation.
        
        Leave empty to list possible values.
        """
        # WARNING : this function should not raise any errors if system well formed
        if configkey is None or configkey == '' :
            print('\n# ExportConfig list keys')
            for key in ExportConfig.config_keys : 
                print(f'- {key}')
            print('For more info, try ExportConfig.doc(configkey) using a key name, listed above.\n')
            return
        doc = f"\n# ExportConfig Doc {configkey}\n"
        if not configkey in ExportConfig.config_keys :
            doc += "Not a valid key."
        else :
            item = ExportConfig.config_keys[configkey]
            # Key ID
            doc += f"Key {configkey} "
            if item[0] == bool : doc += f"enable"
            else               : doc += f"adjust"
            doc += f" {item[2]}.\n## Doc\n"
            # Key type
            doc += f"### Value type\nExpecting a {item[0].__name__}.\n"
            # Key default value
            doc += "### Default value\nDefault value is "
            if item[0] == str : doc += f"\"{item[1]}\".\n"
            else              : doc += f"{item[1]}.\n"
            # Key possible values
            if   len(item) == 3  : pass
            elif item[0] == bool : pass
            else :
                doc += "### Possible values\n"  
                if   item[0] == int : doc += f"Value must be in range [{item[3][0]} ; {item[3][1]}].\n"
                elif item[0] == str :
                    doc += "Value must be one which follow :"
                    for value in item[3] : doc += f"\n- \"{value}\" ;"
                    doc += "\n"
        print(doc)