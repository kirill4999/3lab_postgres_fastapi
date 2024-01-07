from config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dbModels import Base,UserEntity


engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    echo=True,
)
AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with sessionmaker(engine, expire_on_commit=True, class_=AsyncSession)() as session:
        new_entry = UserEntity(id = 0, name = "Тайлаков К.Н.", hashed_password = "12434" )
        session.add(new_entry)
        await session.commit()



async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session