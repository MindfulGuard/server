from math import ceil
from mindfulguard.authentication.executors import get_authorization_token
from mindfulguard.core.response_status_codes import BAD_REQUEST, OK

from mindfulguard.database.postgresql.admin import Admin
from mindfulguard.utils import Validation
from tests.api.secure.secure import sha256s


PER_PAGE = 10

class GetUsers:
    def __init__(self):
        self.__admin_db = Admin()

    async def execute(self,token:str,page:int):
        validation = Validation()
        tokenf:str = get_authorization_token(token)
        pages_db:int = await self.__get_pages()
        calcul_page = self.__calculate_page(page)


        if validation.validate_token(tokenf) == False:
            return (0,0,([],BAD_REQUEST))

        return (
        await self.__get_pages(),
        await self.__admin_db.get_count_users(), 
        await self.__admin_db.get_all_users(
            sha256s(tokenf),
            calcul_page[0],
            calcul_page[1]
        )
        )

    def __calculate_page(self,page:int)->tuple[int, int]:
        """
        Returns:
            (limit,offset)
        """
        pp = (PER_PAGE*page)
        return (pp,pp-PER_PAGE)

    async def __get_pages(self)->int:
        return ceil(await self.__admin_db.get_count_users() / PER_PAGE)
    
class SearchUsers:
    def __init__(self,key:str,value:str):
        self.__key = key
        self.__value = value
        self.__dict = {
            "id":"u_id",
            "username":"u_login"
        }
        self.__admin_db = Admin()

    async def execute(self,token:str):
        validation = Validation()
        tokenf:str = get_authorization_token(token)

        if (
            validation.validate_token(tokenf) == False
            or self.__key not in self.__dict
            or self.__key == "id" and not validation.validate_is_uuid(self.__value)
        ):
            return ({},BAD_REQUEST)
    
        return await self.__admin_db.search_users(sha256s(tokenf),self.__dict[self.__key],self.__value)