from database.sqllite_db import engine, User
from sqlalchemy.orm import Session
from sqlalchemy import select
import asyncio




async def add_user(user_id,name,gender,age, wish_news):

    with Session(engine) as session:
        stmt = select(User).where(User.user_id == user_id)
        if not session.scalar(stmt):

            user =User(user_id,name,gender,age, wish_news)
            session.add(user)

        session.commit()

async def get_list_user_id():
    with Session(engine) as session:
        stmt = select(User.user_id)
        return session.scalars(stmt).all()

async def get_user(user_id):
    with Session(engine) as session:
        stmt = select(User).where(User.user_id == user_id)
        return session.scalar(stmt)








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
