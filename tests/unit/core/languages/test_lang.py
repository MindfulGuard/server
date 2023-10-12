from pyparsing import Any
from mindfulguard.core.languages.package_reader import Files

def is_list(variable:list)->bool:
    if isinstance(variable, list):
        return True
    return False

def is_dict(variable:dict)->bool:
    if isinstance(variable, dict):
        return True
    return False

def files():
    files = Files()
    file_names:list[str] = files.__get_file_names()
    msg:dict[str, Any] = files.get("server_error")

    return (is_list(file_names),is_dict(msg))

def test_lang():
    is_list:bool = files()[0]
    is_dict:bool = files()[1]

    assert is_list == True
    assert is_dict == True