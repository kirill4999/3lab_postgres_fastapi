from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime


class CommentModel(BaseModel):
    id: Optional[int]
    id_user: Optional[int]
    time: Optional[datetime]
    data: Optional[str]
