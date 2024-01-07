from typing import Optional
from pydantic import BaseModel


class UserModel(BaseModel):
    id: Optional[int]
    name: Optional[str]
    hashed_password: Optional[str]
