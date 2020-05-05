
import json

def getconfig(): 
    '''
        This method reads the config file set in the config section and return a dict
        @return config
    '''
    config_file_path = "config/project_recipe_config.json"

    with open(config_file_path,'r') as cfg: 
        config = json.load(cfg)
    
    return config