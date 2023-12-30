from mindfulguard.classes.models import ModelBase


class ModelSafe(ModelBase):
    def __init__(self):
        super().__init__()
        self._id: str
        self.__user_id: str
        self.__name: str
        self.__description: str
        self.__created_at: int
        self.__updated_at: int

    @property
    def id(self) -> str:
        return self._id
    
    @id.setter
    def id(self, value: str) -> None:
        if not self._validation.is_uuid(value):
            raise ValueError('The value is not a uuid')
        self._id = value

    @property
    def user_id(self) -> str:
        return self.__user_id
    
    @user_id.setter
    def user_id(self, value: str) -> None:
        if not self._validation.is_uuid(value):
            raise ValueError('The value is not a uuid')
        self.__user_id = value

    @property
    def name(self) -> str:
        return self.__name
    
    @name.setter
    def name(self, value: str) -> None:
        NAME_LENGTH = 64
        if len(value) > NAME_LENGTH:
            raise ValueError(f'Maximum name length {NAME_LENGTH} characters, value length: {len(value)}')
        self.__name = value

    @property
    def description(self) -> str:
        return self.__description
    
    @description.setter
    def description(self, value: str) -> None:
        DESCRIPTION_LENGTH = 580
        if len(value) > DESCRIPTION_LENGTH:
            raise ValueError(f'Maximum description length {DESCRIPTION_LENGTH} characters, value length: {len(value)}')
        self.__description = value

    @property
    def created_at(self) -> int:
        return self.__created_at
    
    @created_at.setter
    def created_at(self, value: int) -> None:
        self.__created_at = value

    @property
    def updated_at(self) -> int:
        return self.__updated_at
    
    @updated_at.setter
    def updated_at(self, value: int) -> None:
        self.__updated_at = value