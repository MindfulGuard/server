from typing import Any
from mindfulguard.core.languages.package_reader import Files

def is_list(variable:list)->bool:
    if isinstance(variable, list):
        return True
    return False

def is_dict(variable:dict)->bool:
    if isinstance(variable, dict):
        return True
    return False

def files()-> bool:
    __files = Files()
    msg:dict[str, Any] = __files.get("server_error")

    return is_dict(msg)

def test_lang():
    is_dict:bool = files()

    assert is_dict == True