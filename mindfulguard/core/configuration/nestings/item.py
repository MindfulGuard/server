from mindfulguard.core.configuration.utils import concatenate_with_dot


class Lengths:
    def __init__(self,root_block:str,server_configuration):
        self.__block:str = concatenate_with_dot(root_block,"lengths")
        self.__config = server_configuration
    def get_title_length(self)->int:
        return self.__config.read_configuration(self.__block,'title_length')
    def get_notes_length(self)->int:
        return self.__config.read_configuration(self.__block,'notes_length')
    def get_tags_array_length(self)->int:
        return self.__config.read_configuration(self.__block,'tags_array_length')
    def get_tags_length(self)->int:
        return self.__config.read_configuration(self.__block,'tags_length')    
    def get_sections_array_length(self)->int:
        return self.__config.read_configuration(self.__block,'sections_array_length')
    def get_fields_array_length(self)->int:
        return self.__config.read_configuration(self.__block,'fields_array_length')
    def get_label_length(self)->int:
        return self.__config.read_configuration(self.__block,'label_length')
    def get_value_length(self)->int:
        return self.__config.read_configuration(self.__block,'value_length')
    def get_section_length(self)->int:
        return self.__config.read_configuration(self.__block,'section_length')

class Categories:
    def __init__(self,root_block:str,server_configuration):
        self.__block:str = concatenate_with_dot(root_block,"categories")
        self.__config = server_configuration
    def get_array(self)->list[str]:
        return self.__config.read_configuration(self.__block,'array')

class Types:
    def __init__(self,root_block:str,server_configuration):
        self.__block:str = concatenate_with_dot(root_block,"types")
        self.__config = server_configuration
    def get_array(self)->list[str]:
        return self.__config.read_configuration(self.__block,'array')