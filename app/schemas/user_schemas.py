from pydantic import Field, BaseModel
from typing import Annotated, Optional


class RegSchemas(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=30)]
    number: Annotated[str, Field(min_length=11, max_length=11)]
    telegram_id: str
    password: Annotated[str, Field(min_length=8, max_length=30)]
    address: str
    housing_complex_id: Optional[int] = None


class LogSchemas(BaseModel):
    number: Annotated[str, Field(min_length=11, max_length=11)]
    password: Annotated[str, Field(min_length=8, max_length=30)]


class LogResponseSchemas(BaseModel):
    id: int


class UpdateUserSchema(BaseModel):
    name: Optional[str] = None
    number: Optional[str] = None
    telegram_id: Optional[str] = None
    password: Optional[str] = None
    address: Optional[str] = None