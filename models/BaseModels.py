from pydantic import BaseModel
from enum import Enum


class Tags(Enum):
    users = "users"
    comments = "comments"


class NewResponse(BaseModel):
    message: str