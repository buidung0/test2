from typing import Optional

from pydantic import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import APP_NAME, APP_VERSION


class Settings(BaseSettings):
    APP_NAME: str = APP_NAME
    APP_VERSION: str = APP_VERSION
    DATABASE_FOLDER: Optional[str] = "storages"


class DatabaseManager:
    def __init__(self, base_db_url: str, settings: Settings):
        self.base_engine = self.create_engine(base_db_url)
        self.settings = settings
        self.engines = {"base": self.base_engine}

    @staticmethod
    def create_engine(db_url: str):
        return create_engine(db_url, connect_args={"check_same_thread": False})

    def get_engine(self, db_url: str):
        if db_url in self.engines:
            return self.engines[db_url]

        engine = self.create_engine(db_url)
        self.engines[db_url] = engine
        return engine

    def get_db(self, db_url: Optional[str] = None):
        if db_url is None:
            engine = self.base_engine
        else:
            engine = self.get_engine(db_url)

        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        try:
            yield session
        finally:
            session.close()
