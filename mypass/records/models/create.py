from pydantic import BaseModel

class Fields(BaseModel):
    type:str
    label:str
    value:str

class Sections(BaseModel):
    section:str
    fields:list[Fields]


class Item(BaseModel):
    title:str
    category:str
    notes:str
    tags:list[str]
    sections:list[Sections]