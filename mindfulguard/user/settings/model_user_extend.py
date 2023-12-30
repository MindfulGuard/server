from mindfulguard.classes.models.user import ModelUser

class ModelUserExtend(ModelUser):
    def __init__(self):
        super().__init__()
        self.__old_secret_string: str
        self.__new_secret_string: str

    @property
    def old_secret_string(self) -> str:
        return self.__old_secret_string
    
    @old_secret_string.setter
    def old_secret_string(self, value: str) -> None:
        if (
            not self._validation.is_secret_string(value)
        ):
            raise ValueError(f'Secret_string must be equal to 64 characters, length is {len(value)}')
        self.__old_secret_string = str(self._security.hash().sha(value))

    @property
    def new_secret_string(self) -> str:
        return self.__new_secret_string
    
    @new_secret_string.setter
    def new_secret_string(self, value: str) -> None:
        if (
            not self._validation.is_secret_string(value)
        ):
            raise ValueError(f'Secret_string must be equal to 64 characters, length is {len(value)}')
        self.__new_secret_string = str(self._security.hash().sha(value))