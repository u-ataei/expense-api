from sqlalchemy import create_engine, Column, String, Integer, Float
from sqlalchemy.orm import DeclarativeBase, Session
from core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass


class Expense(Base):
    __tablename__ = "expense"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(255))
    amount = Column(Float)


def db_init():
    Base.metadata.create_all(engine)


def db_session():
    with Session(engine) as session:
        yield session
