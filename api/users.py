from fastapi import APIRouter, Body
from models.userModels import MainUser, MainUserdb, NewResponse
from typing import Union, Annotated

users_router = APIRouter()

users_list = [
    MainUserdb(name="Иван", id=1, password="214214фвыафыва"),
    MainUserdb(name="Пётр", id=9, password="выафпфывфафыва")
]


def password_generation(code: str):
    result = code * 228


def find_user(identifier: int) -> Union[MainUserdb, None]:
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
    return users_list