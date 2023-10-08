import random
import string

from pydantic import BaseModel, Field
from dataclasses import dataclass, field


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserDisplay(BaseModel):
    username: str
    email: str


class NewsSchema(BaseModel):
    created_by: str = Field(..., min_length=3, max_length=140)
    context: str = Field(..., min_length=3, max_length=4096)
    published_date: str = Field(..., min_length=3, max_length=32)


class NewsDB(NewsSchema):
    id: int

