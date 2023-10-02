import mindfulguard.core.configuration as configuration

class InitConf:
    def __init__(self):
        self.__config = configuration.ServerConfiguration()
    def get(self):
        return configuration.Item(self.__config)