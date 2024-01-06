from sqlalchemy import create_engine
from config import settings
from dbContext import Base


ur_s = settings.POSTGRES_DATABASE_URLS
print(ur_s)
engine_s = create_engine(ur_s, echo=True)


def create_tables():
    Base.metadata.drop_all(engine_s)
    Base.metadata.create_all(engine_s)
