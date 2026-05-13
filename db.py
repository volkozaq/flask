import atexit
import os
import datetime

from sqlalchemy import create_engine, Integer, String, DATETIME, func, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, MappedColumn, mapped_column


POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "flask")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    mapped_column()
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)

    @property
    def id_dict(self):
        return {"id": self.id}

class Advert(Base):
    __tablename__ = "adverts"

    title: MappedColumn[str] = mapped_column(String, nullable=False)
    description: MappedColumn[str] = mapped_column(String, nullable=False)
    created_at: MappedColumn[datetime.datetime] = mapped_column(DateTime,
                                                       default = datetime.datetime.now
                                                       )
    owner: MappedColumn[str] = mapped_column(String, nullable=False)

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "owner": self.owner
        }

Base.metadata.create_all(bind=engine)
atexit.register(engine.dispose)
