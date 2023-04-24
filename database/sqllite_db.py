from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy import ForeignKey, create_engine, Column, Integer, String, ForeignKey, Boolean



# строка подключения
sqlite_database = "sqlite:///database.db"
# создаем движок SqlAlchemy
engine = create_engine(sqlite_database, echo=True)
# создаем модель, объекты которой будут храниться в бд
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, index = True)
    user_id = Column(Integer, unique=True, nullable=False)
    name = Column(String)
    wish_news = Column(Boolean, default=True)

    def __init__(self, user_id, name, wish_news = True):
        self.user_id = user_id
        self.name = name
        wish_news = wish_news

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.use_id, self.wish_news)

class Speciality(Base):
    __tablename__ = "specialties"


Base.metadata.create_all(engine)