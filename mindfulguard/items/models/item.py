from pydantic import BaseModel, field_validator, constr
from mindfulguard.core.response_status_codes import INTERNAL_SERVER_ERROR
from mindfulguard.database.postgresql.settings import Settings

from pydantic_async_validation import async_field_validator, AsyncValidationModelMixin

import mindfulguard.items.models as const

"""
Attention "pylance" may swear with the error "Call expression not allowed in type expression", but the code remains working
"""

class Fields(AsyncValidationModelMixin,BaseModel):
    type: constr(min_length=1, max_length=20)
    label:constr(min_length=0, max_length=const.LABEL_LENGTH)
    value:constr(min_length=0, max_length=const.VALUE_LENGTH)

    @async_field_validator("type")
    async def type_in_types(self, value)-> None:
        types_array =  await Settings().get()
        types = types_array[0]['item_types']
        if types_array[1] == INTERNAL_SERVER_ERROR:
            raise ValueError("Server error")
        if value not in types:
            raise ValueError(f"'{value}' is not an acceptable type")


class Sections(AsyncValidationModelMixin, BaseModel):
    section:constr(min_length=0, max_length=const.SECTION_LENGTH)
    fields:list[Fields]

    @field_validator("fields")
    def fields_(cls, value):
        length = const.FIELDS_ARRAY_LENGTH
        if len(value) > length:
            raise ValueError(f"'{value}' exceeding the length of the array")
        return value

class Item(AsyncValidationModelMixin,BaseModel):
    title:constr(min_length=0, max_length=const.TITLE_LENGTH)
    category:constr(min_length=0, max_length=20)
    notes:constr(min_length=0, max_length=const.NOTES_LENGTH)
    tags:list[str]
    sections:list[Sections]

    @field_validator("sections")
    def validate_sections(cls, value):
        init_count = 0
        sections = const.SECTIONS_ARRAY_LENGTH
        if len(value) > sections:
            raise ValueError(f"'{value}' exceeded the maximum number of sections")
        
        for section in value:
            if section.section == "INIT":
                init_count += 1
        if init_count != 1:
            raise ValueError("There must be exactly one 'INIT' section")
        return value
        
    @async_field_validator("category")
    async def category_in_categories(self, value)-> None:
        category_array = await Settings().get()
        if category_array[1] == INTERNAL_SERVER_ERROR:
            raise ValueError("Server error")
        categories = category_array[0]['item_categories']
        if value not in categories:
            raise ValueError(f"'{value}' is not an acceptable category")

    @field_validator("tags")
    def validate_tags(cls, value):
        tags_length = const.TAGS_LENGTH
        max_tags_length = const.TAGS_ARRAY_LENGTH

        if len(value) > max_tags_length:
            raise ValueError(f"The number of tags exceeds the maximum of {max_tags_length} allowed tags")
        
        for i, string in enumerate(value):
            if len(string) > tags_length or len(string.replace(" ", "").replace("\t", "").replace("\n", "")) == 0:
                raise ValueError(f"Element {i} exceeds the maximum length of {tags_length} characters and it is impossible for the length of the element {i} to be less than 0")
        return value