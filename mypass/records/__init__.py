from mypass.core.languages import Language
from mypass.core.languages.responses import Responses


class Records:
    def __init__(self):
        self.__lang = Language()
        self.__json_responses = Responses(self.__lang)