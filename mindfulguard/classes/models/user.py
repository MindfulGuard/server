from mindfulguard.classes.models import ModelBase

class ModelUser(ModelBase):
    def __init__(self):
        super().__init__()
        self.__id: str
        self.__login: str
        self.__reg_ip: str
        self.__confirm: bool
        self.__created_at: int
        self.__secret_string: str
        self.__admin: bool

    @property
    def id(self) -> str:
        return self.__id
    
    @id.setter
    def id(self, value: str) -> None:
        if not self._validation.is_uuid(value):
            raise ValueError('The value is not a uuid')
        self.__id = value

    @property
    def login(self) -> str:
        return self.__login
    
    @login.setter
    def login(self, value: str) -> None:
        if not self._validation.is_login(value):
            raise ValueError('The value can only be present: hyphen, underscore, Latin characters only')
        self.__login = value

    @property
    def reg_ip(self) -> str:
        return self.__reg_ip
    
    @reg_ip.setter
    def reg_ip(self, value: str) -> None:
        if not self._validation.is_ip(value):
            raise ValueError(f'Invalid ip address {value}')
        self.__reg_ip = value

    @property
    def confirm(self) -> bool:
        return self.__confirm
    
    @confirm.setter
    def confirm(self, value: bool) -> None:
        self.__confirm = value

    @property
    def created_at(self) -> int:
        return self.__created_at
    
    @created_at.setter
    def created_at(self, value: int) -> None:
        self.__created_at = value

    @property
    def secret_string(self) -> str:
        return self.__secret_string
    
    @secret_string.setter
    def secret_string(self, value: str) -> None:
        if not self._validation.is_secret_string(value):
            raise ValueError(f'Secret_string must be equal to 64 characters, length is {len(value)}')
        self.__secret_string = str(self._security.hash().sha(value))

    @property
    def admin(self) -> bool:
        return self.__admin
    
    @admin.setter
    def admin(self, value: bool) -> None:
        self.__admin = value