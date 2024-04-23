from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.responses import HttpResponse

class MiddlewareBase:
    def __init__(self) -> None:
        self._model_token = ModelToken()
        self._http_response = HttpResponse()