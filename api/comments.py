from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.BaseModels import Tags
from models.CommentModel import CommentModel
from dbModels import CommentEntity
from db import get_session
from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

comments_router = APIRouter(tags=[Tags.comments], prefix='/api/comments')


def password_encryption(password: str):
    return pbkdf2_sha256.hash(password)


def entity_to_model(entity: CommentEntity):
    return CommentModel(id = entity.id, id_user = entity.id_user, time = entity.time, data = entity.data)


def model_to_entity(model: CommentModel):
    return CommentEntity(id = model.id, id_user = model.id_user, time = model.time, data = model.data)


@comments_router.get("/{id}", response_model=CommentModel)
async def get_comment(comment_id: int, data_base: Session = Depends(get_session)):
    async with data_base.begin():
        query = select(CommentEntity).where(CommentEntity.id == comment_id)
        executed_query = await data_base.execute(query)
        comment_entity = executed_query.scalar()

    if comment_entity is None:
        raise HTTPException(status_code=404, detail="Комментарий не найден")

    return entity_to_model(comment_entity)


@comments_router.get("/", response_model=List[CommentModel])
async def get_all_comments(data_base: Session = Depends(get_session)):
    async with data_base.begin():
        query = select(CommentEntity)
        executed_query = await data_base.execute(query)
        comment_entities = executed_query.scalars().all()

        if comment_entities is None:
            raise HTTPException(status_code=404, detail="Записи не найдены")

        result = list()
        for entity in comment_entities:
            result.append(entity_to_model(entity))

    return result


@comments_router.post("/", response_model=CommentModel)
async def create_comment(cr_comment: CommentModel, data_base: AsyncSession = Depends(get_session)):
    try:
        comment_entity = model_to_entity(cr_comment)#CommentEntity(name=cr_comment.name, hashed_password=password_encryption(cr_comment.name))
        if comment_entity is None:
            raise HTTPException(status_code=404, detail="Объект не определен")
        async with data_base.begin():
            data_base.add(comment_entity)
            await data_base.commit()

        await data_base.refresh(comment_entity)
        return entity_to_model(comment_entity)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при добавлении {cr_comment}")


@comments_router.delete("/", response_model=str)
async def delete_comment(identifier: int, data_base: AsyncSession = Depends(get_session)):
    try:
        async with data_base.begin():
            query = select(CommentEntity).where(CommentEntity.id == identifier)
            result = await data_base.execute(query)
            comment_additional_info = result.scalar()

            if comment_additional_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            await data_base.delete(comment_additional_info)

        return "ok"
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении: {exc}")


@comments_router.put("/{id}", response_model=CommentModel)
async def update_comment_additional_info(identifier: int, updated_info: CommentModel,
                                      data_base: AsyncSession = Depends(get_session)):
    try:
        async with data_base.begin():
            query = select(CommentEntity).where(CommentEntity.id == identifier)
            result = await data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            existing_info.id = updated_info.id
            existing_info.id_user = updated_info.id_user
            existing_info.data = updated_info.data
            existing_info.time = updated_info.time

        return entity_to_model(existing_info)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении: {exc}")


@comments_router.patch("/{id}", response_model=CommentModel)
async def partial_update_comment_additional_info(identifier: int, updated_info: CommentModel,
                                              data_base: AsyncSession = Depends(get_session)):
    try:
        async with data_base.begin():
            query = select(CommentEntity).where(CommentEntity.id == identifier)
            result = await data_base.execute(query)
            existing_info = result.scalar()

            if existing_info is None:
                raise HTTPException(status_code=404, detail="Запись не найдена")

            if updated_info.id:
                existing_info.id = updated_info.id
            if updated_info.time:
                existing_info.time = updated_info.time
            if updated_info.id_user:
                existing_info.id_user = updated_info.id_user
            if updated_info.data:
                existing_info.data = updated_info.data

        return entity_to_model(existing_info)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ошибка при частичном обновлении: {exc}")
