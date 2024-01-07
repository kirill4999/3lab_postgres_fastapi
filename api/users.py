from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.BaseModels import Tags
from models.UserModel import UserModel
from dbModels import UserEntity
from db import get_session
from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

users_router = APIRouter(tags=[Tags.users], prefix='/api/users')


def password_encryption(password: str):
    return pbkdf2_sha256.hash(password)


def entity_to_model(entity: UserEntity):
    return UserModel(id = entity.id, name = entity.name, hashed_password = entity.hashed_password)


def model_to_entity(model: UserModel):
    return UserEntity(id = model.id, name = model.name, hashed_password = password_encryption(model.hashed_password))


@users_router.get("/{id}", response_model=UserModel)
async def get_user(user_id: int, data_base: Session = Depends(get_session)):
    async with data_base.begin():
        query = select(UserEntity).where(UserEntity.id == user_id)
        executed_query = await data_base.execute(query)
        user_entity = executed_query.scalar()

    if user_entity is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return entity_to_model(user_entity)


@users_router.get("/", response_model=List[UserModel])
async def get_all_users(data_base: Session = Depends(get_session)):
    async with data_base.begin():
        query = select(UserEntity)
        executed_query = await data_base.execute(query)
        user_entities = executed_query.scalars().all()

        if user_entities is None:
            raise HTTPException(status_code=404, detail="Записи не найдены")

        result = list()
        for entity in user_entities:
            result.append(entity_to_model(entity))

    return result


@users_router.post("/", response_model=UserModel)
async def create_user(cr_user: UserModel, data_base: AsyncSession = Depends(get_session)):
    try:
        user_entity = model_to_entity(cr_user)
        if user_entity is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        async with data_base.begin():
            data_base.add(user_entity)
            await data_base.commit()

        await data_base.refresh(user_entity)
        return entity_to_model(user_entity)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении {cr_user}")


@users_router.delete("/", response_model=str)
async def delete_user(identifier: int, data_base: AsyncSession = Depends(get_session)):
    try:
        async with data_base.begin():
            query = select(UserEntity).where(UserEntity.id == identifier)
            result = await data_base.execute(query)
            user_additional_info = result.scalar()

            if user_additional_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            await data_base.delete(user_additional_info)

        return "ok"
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {exc}")


@users_router.put("/{id}", response_model=UserModel)
async def update_user_additional_info(identifier: int, updated_info: UserModel,
                                      data_base: AsyncSession = Depends(get_session)):
    try:
        async with data_base.begin():
            query = select(UserEntity).where(UserEntity.id == identifier)
            result = await data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            existing_info.id = updated_info.id
            existing_info.name = updated_info.name
            existing_info.hash_password = password_encryption(updated_info.hashed_password)

        return entity_to_model(existing_info)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении: {exc}")


@users_router.patch("/{id}", response_model=UserModel)
async def partial_update_user_additional_info(identifier: int, updated_info: UserModel,
                                              data_base: AsyncSession = Depends(get_session)):
    try:
        async with data_base.begin():
            query = select(UserEntity).where(UserEntity.id == identifier)
            result = await data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            if updated_info.id:
                existing_info.id = updated_info.id
            if updated_info.name:
                existing_info.name = updated_info.name
            if updated_info.hashed_password:
                existing_info.hash_password = password_encryption(updated_info.hashed_password)

        return entity_to_model(existing_info)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при частичном обновлении: {exc}")
