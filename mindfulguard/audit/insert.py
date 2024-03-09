from fastapi import Request, logger
from mindfulguard.classes.audit.base import AuditBase
from mindfulguard.exceptions.http import InvalidHttpMethod, InvalidUrlPath
from mindfulguard.net.ip import get_client_ip

class AuditInsert(AuditBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)

    async def execute(
        self,
        token: str,
        device: str,
    ) -> None:
        try:
            self._model_token.token = token
            self._model_audit.ip = get_client_ip(self._request)
            self._model_audit.device = device

            request_method: str = self._request.method.lower()
            request_url_path: str = self._request.url.path
            audit_data = self.__define_audit_data(request_method, request_url_path)

            self._model_audit.object = audit_data[0]
            self._model_audit.action = audit_data[1]

            await self._connection.open()
            await self._pgsql_audit.insert(self._model_token, self._model_audit).execute()
        except ValueError:
            return
        except InvalidHttpMethod:
            return
        except InvalidUrlPath as e:
            logger.logger.warning(e)
            return
        finally:
            await self._connection.close()

    def __define_audit_data(self, request_method: str, request_url_path: str):
        if request_method == 'get':
            raise InvalidHttpMethod(f"Invalid HTTP method: {request_method}")
        else:
            object: str = ''
            action: str = ''

            if request_url_path.startswith('/v1/safe') and request_url_path.endswith('/content'):
                object = self._model_audit.audit_object.file
                if request_method == 'post':
                    action = self._model_audit.audit_action_type.upload
                elif request_method == 'delete':
                    action = self._model_audit.audit_action_type.delete
            elif request_url_path.startswith('/v1/safe') and request_url_path.endswith('/item'):
                object = self._model_audit.audit_object.item
                if request_method == 'post':
                    action = self._model_audit.audit_action_type.create
                elif request_method == 'put':
                    action = self._model_audit.audit_action_type.update
                elif request_method == 'delete':
                    action = self._model_audit.audit_action_type.delete
            elif (
                request_url_path.startswith('/v1/safe')
                and not request_url_path.endswith('/item')
                and not request_url_path.endswith('/content')
            ):
                object = self._model_audit.audit_object.safe
                if request_method == 'post':
                    action = self._model_audit.audit_action_type.create
                elif request_method == 'put':
                    action = self._model_audit.audit_action_type.update
                elif request_method == 'delete':
                    action = self._model_audit.audit_action_type.delete

            elif request_url_path.startswith('/v1/user'):
                object = self._model_audit.audit_object.user
                if request_url_path.startswith('/v1/user/settings'):
                    action = self._model_audit.audit_action_type.update
                else:
                    if request_method == 'post':
                        action = self._model_audit.audit_action_type.create
                    elif request_method == 'put':
                        action = self._model_audit.audit_action_type.update
                    elif request_method == 'delete':
                        action = self._model_audit.audit_action_type.delete

            else:
                raise InvalidUrlPath(f"Invalid url path: {request_url_path}")

            return object, action                

