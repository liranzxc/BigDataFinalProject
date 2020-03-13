import json
def get_config_data():
    with open('config.json') as config_file:
        data = json.load(config_file)
        return data