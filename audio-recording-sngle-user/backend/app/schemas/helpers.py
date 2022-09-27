from pydantic import BaseModel


def lower_camel(string: str) -> str:
    camel = ''.join(word.capitalize() for word in string.split('_'))
    low_camel = camel[0].lower() + camel[1:]
    return low_camel


class BaseConfig(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = lower_camel
        allow_population_by_field_name = True
