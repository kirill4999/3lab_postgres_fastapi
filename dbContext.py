from typing import Union, Annotated
from pydantic import BaseModel, Field, HttpUrl
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from enum import Enum

Base = declarative_base()


class UserEntity(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    hashed_password = Column(String)


class CommentsEntity(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    time = Column(DateTime)
    data = Column(String)