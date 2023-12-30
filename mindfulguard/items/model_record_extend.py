from mindfulguard.classes.models.record import ModelRecord

class ModelRecordExtend(ModelRecord):
    def __init__(self):
        super().__init__()
        self.__old_safe_id: str = ''
        self.__new_safe_id: str = ''
    
    @property
    def old_safe_id(self) -> str:
        return self.__old_safe_id
    
    @old_safe_id.setter
    def old_safe_id(self, value: str) -> None:
        if (
            not self._validation.is_uuid(value)
            or value == self.__new_safe_id
        ):
            raise ValueError('The value is not a uuid or old_safe_id equal new_safe_id')
        self.__old_safe_id = value

    @property
    def new_safe_id(self) -> str:
        return self.__new_safe_id
    
    @new_safe_id.setter
    def new_safe_id(self, value: str) -> None:
        if (
            not self._validation.is_uuid(value)
            or value == self.__old_safe_id
        ):
            raise ValueError('The value is not a uuid or old_safe_id equal new_safe_id')
        self.__new_safe_id = value