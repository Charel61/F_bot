from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import select, ForeignKey, create_engine, Column, Integer, String, ForeignKey, Boolean
from datetime import datetime



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
    user = relationship("Order", cascade="all,delete")

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
    speciality = relationship("Specialist", cascade="all,delete")

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
    specialist = relationship("Order", cascade="all,delete")



    def __init__(self, name, experience, speciality_id):
        self.name = name
        self.experience = experience
        self.speciality_id = speciality_id


    def __repr__(self):
        return "<Specialist('%s','%s','%s')>" % (self.name, self.speciality_id, self.experience)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, unique=True, index = True)

    user_id=Column(Integer, ForeignKey(User.id), nullable=False)
    time_of_order = Column(String, nullable=False)
    specialist_id=Column(Integer, ForeignKey(Specialist.id),nullable=False)
    date_of_vizit=Column(String, nullable=False)
    time_of_vizit=Column(String, nullable=False)


    def __init__(self, user_id, specialist_id, date_of_vizit, time_of_vizit):
        self.user_id = user_id
        self.time_of_order = str(datetime.now())[:16]
        self.specialist_id = specialist_id
        self.date_of_vizit = date_of_vizit
        self.time_of_vizit = time_of_vizit

    def __repr__(self):
        return "<Order('%s','%s','%s','%s')>" % (self.user_id, self.specialist_id, self.date_of_vizit, self.time_of_vizit)









Base.metadata.create_all(engine)
