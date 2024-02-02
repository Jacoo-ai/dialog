import yaml

class Config:

    @staticmethod
    def __load_config(config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    @staticmethod
    def get_config(config_path="config/rasa_config.yaml"):
        return Config.__load_config(config_path)
