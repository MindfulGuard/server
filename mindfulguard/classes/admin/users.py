from http.client import BAD_REQUEST, OK
from typing import Any
from fastapi import Request, Response
from mindfulguard.admin.users.delete_user import AdminUsersDeleteUser
from mindfulguard.classes.authentication import Authentication
from mindfulguard.classes.database import DataBase
from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.responses import HttpResponse
from mindfulguard.database.postgresql.authentication import PostgreSqlAuthentication

class AdminUsers:
    def __init__(
        self,
        response: Response,
        responses: HttpResponse,
        admin_class
    ) -> None:
        self.__http_response: HttpResponse = responses
        self.__response: Response = response
        self.__admin_class = admin_class
    
    async def get_by_page(self, token: str, page: int, per_page: int):
        obj = self.__admin_class.users().get_by_page()
        await obj.execute(
            token,
            page,
            per_page
        )
        self.__response.status_code = obj.status_code
        if obj.status_code != OK:
            return self.__http_response.get(obj.status_code).to_json()

        response: dict[str, Any] = {}
        response['page'] = page
        response['items_per_page'] = per_page
        response['total_pages'] = obj.total_pages
        response['total_users'] = obj.total_users
        response['total_storage_size'] = obj.total_storage_size
        response['list'] = obj.users_list
        return response

    async def search_users(
        self,
        token: str,
        key: str,
        value: str
    ) -> dict[str, Any]:
        obj = self.__admin_class.users().search_users()
        await obj.execute(
            token,
            key,
            value
        )
        self.__response.status_code = obj.status_code
        if obj.status_code != OK:
            return self.__http_response.get(obj.status_code).to_json()
        
        return obj.response
    
    async def create_user(
        self,
        token: str,
        login: str,
        secret_string: str,
        request: Request
    ) -> dict[str, Any]:
        connection = DataBase().postgresql().connection()
        pgsql_auth_admin = PostgreSqlAuthentication(connection)
        model_token = ModelToken()
        authentication_class = Authentication(self.__response, request)
        try:
            model_token.token = token

            db = pgsql_auth_admin.is_auth_admin(model_token)
            await connection.open()
            await db.execute()
            self.__response.status_code = db.status_code
            if db.status_code != OK:
                return self.__http_response.get(db.status_code).to_json()

            return await authentication_class.sign_up(
                login,
                secret_string,
                False
            )
        except ValueError:
            self.__response.status_code = BAD_REQUEST
            return self.__http_response.get(BAD_REQUEST).to_json()
        finally:
            await connection.close()

    async def delete_user(
        self,
        token: str,
        user_id: str
    ):
        obj = AdminUsersDeleteUser()
        await obj.execute(
            token,
            user_id
        )
        self.__response.status_code = obj.status_code
        return self.__http_response.get(obj.status_code).to_json()