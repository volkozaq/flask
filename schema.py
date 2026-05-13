from pydantic import BaseModel, field_validator, ValidationError
from errors import HttpError


class BaseAdvert(BaseModel):
    title: str
    description: str
    owner: str

    @field_validator("title")
    @classmethod
    def normal_title(cls, v):
        if len(v)<3:
            raise ValueError("Title must be at least 3 characters long")
        return v

class CreateAdvert(BaseAdvert):
    pass


class UpdateAdvert(BaseAdvert):
    title: str | None = None
    description: str | None = None
    owner: str | None = None


def validate(schema_cls: type[CreateAdvert, UpdateAdvert], data: dict) -> dict:
    try:
        schema = schema_cls(**data)
        return schema.model_dump(exclude_unset=True)
    except ValidationError as error:
        print(error.errors())
        raise HttpError(400, error.errors()[0]["msg"])