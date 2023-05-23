from database.sqllite_db import engine, User,Speciality, Specialist, Order
from sqlalchemy.orm import Session
from sqlalchemy import select,update
import asyncio
from lexicon.lexicon import LEXICON_RU



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
            print(speciality)
            session.add(speciality)

        session.commit()

async def edit_speciality(id: int, new_name: str):
    with Session(engine) as session:
        stmt = select(Speciality).where(Speciality.id == id)
        if session.scalar(stmt):
            stmt=update(Speciality).where(Speciality.id==id).values(name=new_name)
            session.execute(stmt)

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

            specialist = Specialist(name, experience, speciality_id)
            session.add(specialist)

        else:
            stmt=update(Specialist).where(Specialist.id==id).values(name=name, experience=experience,speciality_id=speciality_id)
            session.execute(stmt)

        session.commit()

# получения списка специалистов по специальности
async def get_list_specialists(speciality_id=None):
    with Session(engine) as session:
        if speciality_id:
            stmt = select(Specialist.name).where(Specialist.speciality_id==speciality_id)
        else:
            stmt = select(Specialist.name)

        return session.scalars(stmt).all()

# Получение информации о специалисте
async def get_specialist(name):
    with Session(engine) as session:
        stmt = select(Specialist.name, Speciality.name, Specialist.experience, Specialist.id ) .join_from(Specialist, Speciality,  Speciality.id==Specialist.speciality_id).where(Specialist.name==name)
        return session.execute(stmt).one()


async def get_specialist_by_id(id: int):
    with Session(engine) as session:
        stmt = select(Specialist.name, Speciality.name, Specialist.experience, Specialist.id ) .join_from(Specialist, Speciality,  Speciality.id==Specialist.speciality_id).where(Specialist.id==id)
        return session.execute(stmt).one()



async def del_specialist(id):
    with Session(engine) as session:

        specialist = session.scalar(select(Specialist).where(Specialist.id==id))
        if specialist:
            session.delete(specialist)
        session.commit()



async def add_order(order):
    with Session(engine, expire_on_commit=False) as session:

        session.add(order)
        session.commit()


async def get_order(id):
    with Session(engine) as session:
        stmt = select(Order).where(Order.id==id)
        return session.scalar(stmt)



async def show_order(order: Order) -> dict|bool:
    with Session(engine) as session:
        stmt = select(User).where(User.user_id==order.user_id)
        user = session.scalar(stmt)
        stmt = select(Specialist.name, Speciality.name) .join_from(Specialist, Speciality,  Speciality.id==Specialist.speciality_id).where(Specialist.id==order.specialist_id)

        specialist = session.execute(stmt).one()




        if order:
            return {
                    'text':f'Имя: {user.name}\n'
                        f'Возраст: {user.age}\n'
                        f'Пол: {LEXICON_RU[user.gender]}\n'
                        f'Дата посещения: {order.date_of_vizit}\n'
                        f'Время посещения: {order.time_of_vizit}\n'
                        f'Специальность: {specialist[1]}\n'
                        f'Специалист: {specialist[0]}\n'
                        f'Дата и время заказа: {order.time_of_order}'
                        }

        else:
            return False
