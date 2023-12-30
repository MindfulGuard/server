from mindfulguard.classes.security import Security
from mindfulguard.validation import Validation


class ModelBase:
    def __init__(self):
        self._validation = Validation()
        self._security = Security()