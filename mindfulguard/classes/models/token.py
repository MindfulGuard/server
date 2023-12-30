from mindfulguard.classes.models import ModelBase


class ModelToken(ModelBase):
    def __init__(self):
        super().__init__()
        self.__id: str
        self.__user_id: str
        self.__token: str
        self.__created_at: int
        self.__updated_at: int
        self.__device: str
        self.__last_ip: str
        self.__expiration: int

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
    def token(self) -> str:
        return self.__token
    
    @token.setter
    def token(self, value: str) -> None:
        PREFIX: str = "Bearer "
        token: str = value.replace(PREFIX, "")
        if not value.startswith(PREFIX) or not self._validation.is_token(token):
            raise ValueError('Invalid token value')
        self.__token = str(self._security.hash().sha(token))

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

    @property
    def device(self) -> str:
        return self.__device
    
    @device.setter
    def device(self, value: str) -> None:
        if not self._validation.is_device(value):
            raise ValueError('Invalid value')
        self.__device = value

    @property
    def last_ip(self) -> str:
        return self.__last_ip
    
    @last_ip.setter
    def last_ip(self, value: str) -> None:
        if not self._validation.is_ip(value):
            raise ValueError(f'Invalid ip address {value}')
        self.__last_ip = value

    @property
    def expiration(self) -> int:
        return self.__expiration
    
    @expiration.setter
    def expiration(self, value: int) -> None:
        MAX_MINUTES: int = 129600
        if 0 > value or value > MAX_MINUTES:
            raise ValueError(f'Invalid value, maximum token expiration time {MAX_MINUTES} minutes')
        self.__expiration = value * 60