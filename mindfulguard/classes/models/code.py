from mindfulguard.classes.models import ModelBase


class ModelCode(ModelBase):
    def __init__(self):
        super().__init__()
        self.__id: str
        self.__user_id: str
        self.__secret_code: str
        self.__backup_codes: list[int]
        self.__created_at: int
        self.__updated_at: int

    @property
    def id(self) -> str:
        return self.__id
    
    @id.setter
    def id(self, value: str) -> None:
        if not self._validation.is_uuid(value):
            raise ValueError('The value is not a uuid')
        self.__id = value

    @property
    def user_id(self) -> str:
        return self.__user_id
    
    @user_id.setter
    def user_id(self, value: str) -> None:
        if not self._validation.is_uuid(value):
            raise ValueError('The value is not a uuid')
        self.__user_id = value

    @property
    def secret_code(self) -> str:
        return self.__secret_code
    
    @secret_code.setter
    def secret_code(self, value: str) -> None:
        self.__secret_code = value

    @property
    def backup_codes(self) -> list[int]:
        return self.__backup_codes
    
    @backup_codes.setter
    def backup_codes(self, value: list[int]) -> None:
        self.__backup_codes = value

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