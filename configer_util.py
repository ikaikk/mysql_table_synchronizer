import configparser


class ConfigUtil:
    __conf = None

    def __init__(self, config_path):
        self.__conf = configparser.ConfigParser()
        self.__conf.read(config_path)

    def get(self, namespace, name):
        return self.__conf.get(namespace, name)
