from pydantic import BaseModel, validator, constr

from mypass.items.models import InitConf

"""
Attention "pylance" may swear with the error "Call expression not allowed in type expression", but the code remains working
"""

init = InitConf()

class Fields(BaseModel):
    type: constr(min_length=1, max_length=20)
    label:constr(min_length=0, max_length=init.get().lengths().get_label_length())
    value:constr(min_length=0, max_length=init.get().lengths().get_value_length())

    @validator("type")
    def type_in_types(cls, value):
        categories = init.get().types().get_array()
        if value not in categories:
            raise ValueError(f"'{value}' is not an acceptable type")
        return value


class Sections(BaseModel):
    section:constr(min_length=0, max_length=init.get().lengths().get_section_length())
    fields:list[Fields]

    @validator("fields")
    def fields_(cls, value):
        length = init.get().lengths().get_fields_array_length()
        if len(value) > length:
            raise ValueError(f"'{value}' exceeding the length of the array")
        return value

class Item(BaseModel):
    title:constr(min_length=0, max_length=init.get().lengths().get_title_length())
    category:constr(min_length=0, max_length=20)
    notes:constr(min_length=0, max_length=init.get().lengths().get_notes_length())
    tags:list[str]
    sections:list[Sections]

    @validator("sections")
    def validate_sections(cls, value):
        init_count = 0
        sections = init.get().lengths().get_sections_array_length()
        if len(value) > sections:
            raise ValueError(f"'{value}' exceeded the maximum number of sections")
        
        for section in value:
            if section.section == "INIT":
                init_count += 1
        if init_count != 1:
            raise ValueError("There must be exactly one 'INIT' section")
        return value
    
    @validator("category")
    def category_in_categories(cls, value):
        categories = init.get().categories().get_array()
        if value not in categories:
            raise ValueError(f"'{value}' is not an acceptable category")
        return value

    @validator("tags")
    def validate_tags(cls, value):
        tags_length = init.get().lengths().get_tags_length()
        max_tags_length = init.get().lengths().get_tags_array_length()

        if len(value) > max_tags_length:
            raise ValueError(f"The number of tags exceeds the maximum of {max_tags_length} allowed tags")
        
        for i, string in enumerate(value):
            if len(string) > tags_length:
                raise ValueError(f"Element {i} exceeds the maximum length of {tags_length} characters")
        return value