from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import engine_s
from dbContext import *
from models.UserModel import UserModel



def get_session():
    with Session(engine_s) as session:
        try:
            yield session
        finally:
            session.close()

users_router = APIRouter()


@users_router.get("/api/users/{user_id}", response_model=UserModel)
def read_user(user_id: int, db: Session = Depends(get_session)):
    user = db.query(UserEntity).filter(UserEntity.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@users_router.post("/users/", response_model=UserModel)
def create_user(user: UserModel, db: Session = Depends(get_session)):
    entity = UserEntity(name = user.name, hashed_password = user.hashed_password)
    db.add(entity)
    db.commit()
    db.refresh(entity)
    user.id = entity.id
    return user


'''def find_user(identifier: int) -> Union[MainUserdb, None]:
    for user in users_list:
        if user.id == identifier:
            return user
    return None


@users_router.get("/api/users", response_model=Union[list[MainUser], None])
def get_users():
    return users_list


@users_router.get("/api/users/{id}", response_model=Union[MainUser, NewResponse])
def get_user(identifier: int):
    user = find_user(identifier)
    print(user)
    if user is None:
        return NewResponse(message="Пользователь не найден")
    return user


@users_router.post("/api/users", response_model=Union[MainUser, NewResponse])
def create_user(item: Annotated[MainUser, Body(embed=True, description="Новый пользователь")]):
    user = MainUserdb(name=item.name, id=item.id, password=password_generation(item.name))
    users_list.append(user)
    return user


@users_router.put("/api/users", response_model=Union[MainUser, NewResponse])
def edit_user(item: Annotated[MainUser, Body(embed=True, description="Изменение данных полльзователя по ID")]):
    user = find_user(item.id)
    if user is None:
        return NewResponse(message="Пользователь не найден")
    user.id = item.id
    user.name = item.name
    return user


@users_router.delete("/api/users/{id}", response_model=Union[list[MainUser], None])
def delete_user(identifier: int):
    user = find_user(identifier)
    if user is None:
        return NewResponse(message="Пользователь не найден")
    users_list.remove(user)
    return users_list'''