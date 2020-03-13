import json


class ConfigService:
    def __init__(self, path_config: str = 'config/config.json'):
        self.path_config = path_config

    def getConfig(self):
        with open(self.path_config) as json_file:
            data = json.load(json_file)
            return data
