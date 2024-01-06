from dotenv import load_dotenv
import os
class Settings:
    POSTGRES_DATABASE_URLS: str
    POSTGRES_DATABASE_URLA: str
    POSTRGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTRGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str


load_dotenv()

settings = Settings()
settings.POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
settings.POSTGRES_DB = os.environ.get("POSTGRES_DB")
settings.POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
settings.POSTRGRES_HOST = os.environ.get("POSTRGRES_HOST")
settings.POSTRGRES_USER = os.environ.get("POSTRGRES_USER")
settings.POSTGRES_DATABASE_URLS = f"postgresql:" \
                            f"//{settings.POSTRGRES_USER}:" \
                            f"{settings.POSTGRES_PASSWORD}" \
                            f"@{settings.POSTRGRES_HOST}/" \
                            f"{settings.POSTGRES_DB}"
