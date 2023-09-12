from mypass.core.configuration.utils import concatenate_with_dot

class Lengths:
    def __init__(self,root_block:str,server_configuration):
        self.__block:str = concatenate_with_dot(root_block,"lengths")
        self.__config = server_configuration
    def get_name_length(self)->int:
        return self.__config.read_configuration(self.__block,'name_length')
    def get_description_length(self)->int:
        return self.__config.read_configuration(self.__block,'description_length')