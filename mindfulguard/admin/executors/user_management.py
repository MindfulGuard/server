from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import BAD_REQUEST, INTERNAL_SERVER_ERROR, OK
from mindfulguard.core.security import sha256s
from mindfulguard.core.security.totp import NUMBER_OF_BACKUP_CODES, Totp
from mindfulguard.database.postgresql.admin import Admin
from mindfulguard.database.postgresql.authentication import Authentication
from mindfulguard.database.postgresql.user.settings import Settings
from mindfulguard.core.s3 import S3
from mindfulguard.utils import Validation


class CreateUser:
    def __init__(self):
        self.__admin_db = Admin()

    async def execute(
            self,
            token:str,
            login:str,
            secret_string:str,
            ip:str,
            confirm:bool
        ):
        validation = Validation()
        tokenf:str = get_authorization_token(token)

        if (
            validation.validate_token(tokenf) == False
            or validation.validate_secret_string(secret_string) == False
            or validation.validate_login(login)==False
        ):
            return ("",[],BAD_REQUEST)

        iadm = await self.__admin_db.is_admin(sha256s(tokenf))
        if iadm!=OK:
            return ("",[],iadm)
        
        totp = Totp("")
        secret_code:str = totp.generate_secret_code()
        backup_codes:list[int] = totp.generate_backup_codes(NUMBER_OF_BACKUP_CODES)

        auth = await Authentication().sign_up(
            login,
            sha256s(secret_string),
            ip,
            confirm,
            secret_code,
            backup_codes
        )

        return (secret_code,backup_codes,auth)
    
class DeleteUser:
    def __init__(self):
        self.__admin_db = Admin()

    async def execute(
            self,
            token:str,
            user_id:str
        ):
        validation = Validation()
        tokenf:str = get_authorization_token(token)

        if (
            validation.validate_token(tokenf) == False
            or validation.validate_is_uuid(user_id) == False
        ):
            return BAD_REQUEST

        iadm = await self.__admin_db.is_admin(sha256s(tokenf))
        if iadm!=OK:
            return iadm

        search_user= await Admin().search_users(sha256s(tokenf),"u_id",user_id)
        if search_user[1] != OK:
            return INTERNAL_SERVER_ERROR
        get_user_login:str = search_user[0]['username']
        delete:int = await Admin().delete_user_admin(
            user_id
        )
        s3_ = S3(get_user_login)

        if delete == OK:
            s3_.object().delete_all_objects()
            s3_.bucket().delete_bucket()
        return delete