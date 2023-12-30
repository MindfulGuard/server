from mindfulguard.classes.models import ModelBase


class ModelSettings(ModelBase):
    def __init__(self):
        super().__init__()
        self.__id: str
        self.__key: str
        self.__value: str
    
    @property
    def id(self) -> str:
        return self.__id
    
    @id.setter
    def id(self, value: str) -> None:
        self.__id = value

    @property
    def key(self) -> str:
        return self.__key
    
    @key.setter
    def key(self, value: str) -> None:
        self.__key = value

    @property
    def value(self) -> str:
        return self.__value
    
    @value.setter
    def value(self, value: str) -> None:
        self.__value = value