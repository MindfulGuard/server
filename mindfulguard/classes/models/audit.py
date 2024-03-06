from mindfulguard.classes.models import ModelBase

class TypeAuditObject:
    @property
    def safe(self):
        return 'safe'

    @property
    def item(self):
        return 'item'

    @property
    def file(self):
        return 'file'
    
    @property
    def user(self):
        return 'user'
    
class TypeAuditActionStatus:
    @property
    def create(self):
        return 'create'

    @property
    def update(self):
        return 'update'
    
    @property
    def delete(self):
        return 'delete'

    @property
    def download(self):
        return 'download'

    @property
    def upload(self):
        return 'upload'
    
    @property
    def sign_up(self):
        return 'sign_up'

    @property
    def sign_in(self):
        return 'sign_in'

    @property
    def sign_out(self):
        return 'sign_out'

class ModelAudit(ModelBase):
    def __init__(self):
        super().__init__()
        self.__id: str
        self.__user_id: str
        self.__created_at: int
        self.__ip: str
        self.__object: str
        self.__action: str
        self.__device: str

    @property
    def audit_object(self) -> TypeAuditObject:
        return TypeAuditObject()
    
    @property
    def audit_action_type(self) -> TypeAuditActionStatus:
        return TypeAuditActionStatus()

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
    def created_at(self) -> int:
        return self.__created_at
    
    @created_at.setter
    def created_at(self, value: int) -> None:
        self.__created_at = value

    @property
    def ip(self) -> str:
        return self.__ip
    
    @ip.setter
    def ip(self, value: str) -> None:
        if not self._validation.is_ip(value):
            raise ValueError(f'Invalid ip address {value}')
        self.__ip = value
        

    @property
    def object(self) -> str:
        return self.__object
    

    @object.setter
    def object(self, value: str) -> None:
        """Use TypeAuditObject"""

        self.__object = value

    @property
    def action(self) -> str:
        return self.__action
    

    @action.setter
    def action(self, value: str) -> None:
        """Use TypeAuditActionStatus"""

        self.__action = value

    @property
    def device(self) -> str:
        return self.__device
    
    @device.setter
    def device(self, value: str) -> None:
        if not self._validation.is_device(value):
            raise ValueError('Invalid value')
        self.__device = value