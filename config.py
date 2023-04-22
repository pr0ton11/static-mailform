import os
import yaml

class Singleton(type):
    """ Metaclass for Singleton """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=Singleton):
    """ Provides configuration """

    def __init__(self):
        self.config = {}

    def from_yaml(self, path: str):
        """ Loads configuration from YAML configuration file """
        if os.path.isfile(path):
            with open(path) as yaml_file:
                self.config = yaml.safe_load(yaml_file)
        else:
            raise FileNotFoundError(f"Configuration file {path} not found")

    def get_env(key):
        """ Checks if variable is found in environment with prefix CONFIG_ and returns its value | None"""
        return os.getenv(f"CONFIG_{key}")

    def get(self, key) -> str | None:
        """ String representation of the configuration value """
        if Config.get_env(key):
            return Config.get_env(key)
        result = Config.traverse_dict(self.config, key)
        if result:
            if isinstance(result, str):
                return result
        return None
    
    def get_int(self, key) -> int | None:
        """ Integer representation of the configuration value """
        if self.get(key):
            if self.get(key).isnumeric():
                return int(self.get(key))
        result = Config.traverse_dict(self.config, key)
        if result:
            if isinstance(result, str):
                if result.isnumeric():
                    return int(result)
                else:
                    raise ValueError(f"Expected integer value in configuration key {key}")
        return None
    
    def get_list(self, key) -> list | None:
        """ List representation of the configuration value """
        if self.get(key):
            if ',' in self.get(key):
                return self.get(key).split(',')
            else:
                raise ValueError(f"Expected a comma seperated list in configuration key {key}")
        
    def traverse_dict(data: dict, key: str) -> str | None:
        """ Traverses a dict based on a given '.' delimeter based key """
        key_parts = key.split('.')
        if len(key_parts) == 1:
            return data[key] if key in data else None
        # Get the next key part and check if data contains this key as dict
        next_key = key_parts[0]
        if next_key in data and isinstance(data[next_key], dict):
            return Config.traverse_dict(data[next_key], ".".join(key_parts[1:]))
        else:
            return None
