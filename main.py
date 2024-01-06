from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from api.users import users_router
from db import create_tables




create_tables()
app = FastAPI(
    description="Задание реализующее CRUD на FastAPI. Сделал Тайлаков Кирилл"
)

app.include_router(users_router, tags=["Users"])


@app.get("/", response_class=PlainTextResponse, tags=["root"])
def root_page():
    return "Добро пожаловать!"