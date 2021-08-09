from pydantic import BaseModel


# Base schema with map from camelCase to snake_case
def to_camel(string: str) -> str:
    words = string.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
