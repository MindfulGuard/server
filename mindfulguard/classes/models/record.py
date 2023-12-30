from typing import Any
from mindfulguard.classes.models import ModelBase


class ModelRecord(ModelBase):
    def __init__(self):
        super().__init__()
        self.__id: str
        self.__safe_id: str
        self.__user_id: str
        self.__title: str
        self._item: dict[str, Any]
        self.__notes: str
        self.__tags: list[str]
        self.__created_at: int
        self.__updated_at: int
        self.__category: str
        self.__favorite: bool

    @property
    def id(self) -> str:
        return self.__id
    
    @id.setter
    def id(self, value: str) -> None:
        if not self._validation.is_uuid(value):
            raise ValueError('The value is not a uuid')
        self.__id = value

    @property
    def safe_id(self) -> str:
        return self.__safe_id
    
    @safe_id.setter
    def safe_id(self, value: str) -> None:
        if not self._validation.is_uuid(value):
            raise ValueError('The value is not a uuid')
        self.__safe_id = value

    @property
    def user_id(self) -> str:
        return self.__user_id
    
    @user_id.setter
    def user_id(self, value: str) -> None:
        if not self._validation.is_uuid(value):
            raise ValueError('The value is not a uuid')
        self.__user_id = value

    @property
    def title(self) -> str:
        return self.__title
    
    @title.setter
    def title(self, value: str) -> None:
        self.__title = value

    @property
    def item(self) -> dict[str, Any]:
        return self._item
    
    @item.setter
    def item(self, value: dict[str, Any]) -> None:
        self._item = value

    @property
    def notes(self) -> str:
        return self.__notes
    
    @notes.setter
    def notes(self, value: str) -> None:
        self.__notes = value

    @property
    def tags(self) -> list[str]:
        return self.__tags
    
    @tags.setter
    def tags(self, value: list[str]) -> None:
        self.__tags = value

    @property
    def created_at(self) -> int:
        return self.__created_at
    
    @created_at.setter
    def created_at(self, value: int) -> None:
        self.__created_at = value

    @property
    def updated_at(self) -> int:
        return self.__updated_at
    
    @updated_at.setter
    def updated_at(self, value: int) -> None:
        self.__updated_at = value

    @property
    def category(self) -> str:
        return self.__category
    
    @category.setter
    def category(self, value: str) -> None:
        self.__category = value

    @property
    def favorite(self) -> bool:
        return self.__favorite
    
    @favorite.setter
    def favorite(self, value: bool) -> None:
        self.__favorite = value