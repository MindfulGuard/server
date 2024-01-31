from mindfulguard.classes.models.token import ModelToken
from mindfulguard.classes.responses import Responses

class MiddlewareBase:
    def __init__(self) -> None:
        self._model_token = ModelToken()
        self._responses = Responses()