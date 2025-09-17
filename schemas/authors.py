from pydantic import BaseModel, ConfigDict

class BaseAuthorSchema(BaseModel):
    first_name: str
    last_name: str
    birth_year: int

class AuthorSchema(BaseAuthorSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)

class AuthorCreateSchema(BaseAuthorSchema):
    pass
