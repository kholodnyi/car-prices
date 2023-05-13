from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from config import settings

Engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,  # max amount of connections in a pool
    max_overflow=70,  # for prime time
    pool_recycle=60,  # seconds
    pool_timeout=2  # seconds
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)

Base = declarative_base()


class CustomBase(Base):
    __abstract__ = True

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def _init_db():
    Base.metadata.create_all(bind=Engine)
