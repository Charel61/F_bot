from database.sqllite_db import engine, User,Speciality, Specialist
from sqlalchemy.orm import Session
from sqlalchemy import select
import asyncio


# aДобавляет пользователя в базу данных

async def add_user(user_id,name,gender,age, wish_news):

    with Session(engine) as session:
        stmt = select(User).where(User.user_id == user_id)
        if not session.scalar(stmt):

            user =User(user_id,name,gender,age, wish_news)
            session.add(user)

        session.commit()


# возвращает список id пользователей
async def get_list_user_id():
    with Session(engine) as session:
        stmt = select(User.user_id)
        return session.scalars(stmt).all()

async def get_user(user_id):
    with Session(engine) as session:
        stmt = select(User).where(User.user_id == user_id)
        return session.scalar(stmt)

# изменяет пользователя

async def change_user(user_id: int ,name: str | None,gender: str | None, age:  int | None, wish_news: bool | None):
    with Session(engine) as session:
        stmt = select(User).where(User.user_id == user_id)
        if session.scalar(stmt):

            user = session.scalar(stmt)
            user.name = name
            user.gender = gender
            user.age = age
            user.wish_news = wish_news
        session.commit()


# Добавление специальности
async def add_speciality(name: str):
    with Session(engine) as session:
        stmt = select(Speciality).where(Speciality.name == name)
        if not session.scalar(stmt):

            speciality =Speciality(name)
            session.add(speciality)

        session.commit()
# получение специальности по id
async def get_speciality(id: int):
    with Session(engine) as session:
        stmt = select(Speciality.name).where(Speciality.id==id)
        return session.scalar(stmt)

async def get_speciality_id(name):
    with Session(engine) as session:
        stmt = select(Speciality.id).where(Speciality.name==name)
        return session.scalar(stmt)



# Получение списка специальностей
async def get_list_specialities():
    with Session(engine) as session:
        stmt = select(Speciality.name)
        return session.scalars(stmt).all()


# Добавление специалиста
async def add_specialist(name: str, experience:int, speciality_id: int):
    with Session(engine) as session:
        stmt = select(Specialist).where(Specialist.name == name, Specialist.speciality_id == speciality_id)
        if not session.scalar(stmt):

            speciality = Specialist(name, experience, speciality_id)
            session.add(speciality)

        session.commit()

# получения списка специалистов по специальности
async def get_list_specialists(speciality_id):
    with Session(engine) as session:
        stmt = select(Specialist.name).where(Specialist.speciality_id==speciality_id)
        return session.scalars(stmt).all()









# list_speciality=asyncio.run(get_list_specialists(1))
# print(list_speciality)
