from pydantic_async_validation import async_field_validator, AsyncValidationModelMixin
from pydantic import BaseModel, field_validator, constr
from mindfulguard.settings import Settings

TITLE_LENGTH: int = 512
NOTES_LENGTH: int = 1024
TAGS_ARRAY_LENGTH: int = 11
TAGS_LENGTH: int = 256
SECTIONS_ARRAY_LENGTH: int = 64
SECTION_LENGTH: int = 256
FIELDS_ARRAY_LENGTH: int = 64
LABEL_LENGTH: int = 64
VALUE_LENGTH: int = 1024

class ModelRecordSettings:
    def __init__(self) -> None:
        self.settings = Settings()

class Fields(AsyncValidationModelMixin, BaseModel):
    type: constr(min_length = 1, max_length = 20)
    label: constr(min_length = 0, max_length = LABEL_LENGTH)
    value: constr(min_length = 0, max_length = VALUE_LENGTH)

    @async_field_validator("type")
    async def type_in_types(self, value)-> None:
        model_record_settings = ModelRecordSettings()
        settings = await model_record_settings.settings.get()

        if value not in settings['item_types']:
            raise ValueError(f"'{value}' is not an acceptable type")

class Sections(AsyncValidationModelMixin, BaseModel):
    section: constr(min_length=0, max_length=SECTION_LENGTH)
    fields: list[Fields]

    @field_validator("fields")
    def fields_(cls, value):
        length = FIELDS_ARRAY_LENGTH
        if len(value) > length:
            raise ValueError(f"'{value}' exceeding the length of the array")
        return value

class Item(AsyncValidationModelMixin, BaseModel):
    title: constr(min_length = 0, max_length = TITLE_LENGTH)
    category: constr(min_length = 0, max_length = 64)
    notes: constr(min_length = 0, max_length = NOTES_LENGTH)
    tags: list[str]
    sections: list[Sections]

    @field_validator("sections")
    def validate_sections(cls, value):
        init_count = 0
        sections = SECTIONS_ARRAY_LENGTH
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
        model_record_settings = ModelRecordSettings()
        settings = await model_record_settings.settings.get()
        if (
            value not in settings['item_categories']
            or len(value.replace(' ', '')) == 0
        ):
            raise ValueError(f"'{value}' is not an acceptable category")

    @field_validator("tags")
    def validate_tags(cls, value):
        tags_length = TAGS_LENGTH
        max_tags_length = TAGS_ARRAY_LENGTH

        if len(value) > max_tags_length:
            raise ValueError(f"The number of tags exceeds the maximum of {max_tags_length} allowed tags")
        
        for i, string in enumerate(value):
            if len(string) > tags_length or len(string.replace(" ", "").replace("\t", "").replace("\n", "")) == 0:
                raise ValueError(f"Element {i} exceeds the maximum length of {tags_length} characters and it is impossible for the length of the element {i} to be less than 0")
        return value