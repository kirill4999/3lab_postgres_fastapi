import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from db import init_db
from api.users import users_router
from models.UserModel import UserModel
from db import get_session
from api.comments import comments_router


app = FastAPI(
    description="Задание реализующее CRUD на FastAPI. Выполнил Тайлаков К.Н."
)

app.include_router(users_router)
app.include_router(comments_router)




async def startup_event():
    await init_db()




app.add_event_handler("startup", startup_event)


@app.get("/", response_class=PlainTextResponse, tags=["Main controller"])
def root_page():
    return "Добро пожаловать!"


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    loop.close()


if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8000)
    main()