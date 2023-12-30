from mindfulguard.classes.models import ModelBase

class ModelTotpCode(ModelBase):
    def __init__(self):
        super().__init__()
        self.__totp_code: str
    
    @property
    def totp_code(self) -> str:
        return self.__totp_code
    
    @totp_code.setter
    def totp_code(self, value: str) -> None:
        if not self._validation.is_TOTP_code(value):
            raise ValueError('The length of the one-time code must be 6 characters.')
        self.__totp_code = value