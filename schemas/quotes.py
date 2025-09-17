from pydantic import BaseModel
from schemas.authors import AuthorSchema
from typing import Optional


class BaseQuoteSchema(BaseModel):
    text: str

class QuoteSchema(BaseQuoteSchema):
    id: int
    author_id: int
    author: Optional[AuthorSchema] = None

class QuoteCreateSchema(BaseQuoteSchema):
    author_id: int