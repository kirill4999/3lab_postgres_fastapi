from pydantic import BaseModel


class UserModel(BaseModel):
    id: int
    name: str
    hashed_password: str