from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session, relationship
from sqlalchemy import select, ForeignKey, create_engine, Column, Integer, String, ForeignKey, Boolean
import asyncio



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
    gender =  Column(String)
    age = Column(Integer)
    wish_news = Column(Boolean, default=True)

    def __init__(self, user_id, name,gender,age, wish_news ):
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.age = age
        wish_news = wish_news

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.name, self.user_id, self.wish_news)

class Speciality(Base):
    __tablename__ = "specialties"

    id = Column(Integer, primary_key=True, unique=True, index = True)
    name = Column(String, unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


    def __repr__(self):
        return "<Speciality('%s')>" % (self.name)

class Specialist(Base):
    __tablename__ = "specialists"

    id = Column(Integer, primary_key=True, unique=True, index = True)
    name = Column(String, nullable=False)
    experience = Column(String)
    speciality_id = Column(Integer, ForeignKey(Speciality.id))
    speciality = relationship(Speciality, cascade="all,delete")

    def __init__(self, name, experience, speciality_id):
        self.name = name
        self.experience = experience
        self.speciality_id = speciality_id


    def __repr__(self):
        return "<Specialist('%s','%s','%s')>" % (self.name, self.speciality_id, self.experience)


Base.metadata.create_all(engine)

async def add_user(user_id,name,gender,age, wish_news):

    with Session(engine) as session:
        stmt = select(User).where(User.user_id == user_id)
        if not session.scalar(stmt):

            user =User(user_id,name,gender,age, wish_news)
            session.add(user)

        session.commit()

async def change_user(user_id,name,gender,age, wish_news):
    with Session(engine) as session:
        stmt = select(User).where(User.user_id == user_id)
        if session.scalar(stmt):

            user = session.scalar(stmt)
            user.name = name
            user.gender = gender
            user.age = age
            user.wish_news = wish_news
        session.commit()


asyncio.run(change_user(480772923, 'huhuhu', 'male', 34, False))



# with Session(engine) as session:
#     user_id = 48077292
#     stmt = select(User).where(User.user_id == user_id)
#     user = session.scalar(stmt)
#     print(session.scalar(stmt))

    # if session.query(User).filter(User.user_id==user_id).all():
    #     print(session.query(User).filter(User.user_id==user_id).all())
    #    / session.query(User).filter(User.user_id==user_id).update(user_id = 44545)
