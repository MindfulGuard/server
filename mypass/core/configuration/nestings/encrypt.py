from mypass.core.configuration.utils import concatenate_with_dot


class Public:
    def __init__(self,root_block:str,server_configuration):
        self.__block:str = concatenate_with_dot(root_block,"public")
        self.__config = server_configuration
    def configuration(self):
        return Configuration(self.__block,self.__config)

class Configuration:
    def __init__(self,root_block:str,server_configuration):
        self.__block:str = concatenate_with_dot(root_block,"configuration")
        self.__config = server_configuration
    def text(self):
        return Text(self.__block,self.__config)
    
class Text:
    def __init__(self,root_block:str,server_configuration):
        self.__block:str = concatenate_with_dot(root_block,"text")
        self.__config = server_configuration
    def get_begin(self)->str:
        return self.__config.read_configuration(self.__block,'begin')
    def get_end(self)->str:
        return self.__config.read_configuration(self.__block,'end')
    