import json
import os
from typing import Any


class Files:
    def __init__(self):
        self.__PATH_TO_LANGUAGE_PACK:str = "mypass/core/languages/package/"
    def __get_file_names(self)->list[str]:
        """
        returns an array with the names of files contained in the package folder.\n
        Example: ["en.json","ru.json",...]
        """
        file_names_with_extension = []
        with os.scandir(self.__PATH_TO_LANGUAGE_PACK) as entries:
            for entry in entries:
                if entry.is_file() and entry.name.endswith('.json'):
                    file_names_with_extension.append(entry.name)
        
        return file_names_with_extension
    def get(self,key:str)->dict[str,Any]:
        """
        Return:
            {"en":"Message","ru":"Сообщение",...}
        """
        response:dict[str,Any] = {}
        for i in self.__get_file_names():
            with open(self.__PATH_TO_LANGUAGE_PACK+i, "r",encoding='utf-8') as file:
                data = json.load(file)
            try:
                response[i.split('.')[0]] = data[key]
            except:
                response[i.split('.')[0]] = None
        return response