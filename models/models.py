from typing import Any
from datetime import datetime
from sqlalchemy import (select, Column, Integer, Result, CursorResult, Enum, String, ForeignKey,
                        Boolean, DateTime, BIGINT, VARCHAR, BOOLEAN, JSON)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, join, sessionmaker, relationship
from config import CONFIG
from emuns import UserRole

Base = declarative_base()


class BaseMixin(object):
    id = Column(Integer, primary_key=True)

    engine = create_async_engine(f'postgresql+asyncpg://{CONFIG.DATABASE}')
    Session = sessionmaker(bind=engine, class_=AsyncSession)

    def __init__(self, **kwargs) -> None:
        for kw in kwargs.items():
            self.__getattribute__(kw[0])
            self.__setattr__(*kw)

    @staticmethod
    def create_async_session(func):
        async def wrapper(*args, **kwargs):
            async with BaseMixin.Session() as session:
                return await func(*args, **kwargs, session=session)

        return wrapper

    @create_async_session
    async def save(self, session: AsyncSession = None) -> None:
        session.add(self)
        await session.commit()
        await session.refresh(self)

    @classmethod
    @create_async_session
    async def get(cls, pk: int = None, user_id: int = None, session: AsyncSession = None) -> Base:
        stmt = select(cls)
        if pk:
            stmt = stmt.where(cls.id == pk)
        if user_id:
            stmt = stmt.where(cls.user_id == user_id)

        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    @create_async_session
    async def all(cls, order_by: str = 'id', session: AsyncSession = None, **kwargs) -> list[Base]:
        return [obj[0] for obj in await session.execute(select(cls).filter_by(**kwargs).order_by(order_by))]

    @create_async_session
    async def delete(self, session: AsyncSession = None) -> None:
        await session.delete(self)
        await session.commit()

    @classmethod
    @create_async_session
    async def join(cls, right: Base, session: AsyncSession = None, **kwargs) -> Result[Any] | CursorResult[Any]:
        return await session.execute(join(left=cls, right=right).filter_by(**kwargs))


class Dialog(BaseMixin, Base):
    __tablename__ = "dialogs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey("users.id"))
    manager_id = Column(BIGINT, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime)
    is_active = Column(Boolean, nullable=False, default=False)
    msg = Column(JSON, nullable=True)

    user_1 = relationship("User", foreign_keys=[user_id])
    user_2 = relationship("User", foreign_keys=[manager_id])


class User(BaseMixin, Base):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key=True)
    first_name = Column(VARCHAR(length=32), nullable=True)
    last_name = Column(VARCHAR(length=32), nullable=True)
    tg_first_name = Column(VARCHAR(length=64), nullable=True)
    tg_last_name = Column(VARCHAR(length=64), nullable=True)
    tg_username = Column(VARCHAR(length=64), nullable=True)
    phone = Column(VARCHAR(length=64), nullable=True)
    comment = Column(VARCHAR(length=64), nullable=True)
    is_block = Column(BOOLEAN, nullable=False, default=False)
    discounts = Column(BOOLEAN, default=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    first_gift_name = Column(VARCHAR(length=100), nullable=True)
    is_webinar = Column(BOOLEAN, default=False)
    mini_courses = relationship("MiniCourse", back_populates="user")
    calculations = relationship("SavingCalculation", back_populates="user")

    def __str__(self) -> str:
        return self.full_name

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Manager(BaseMixin, Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BIGINT, ForeignKey("users.id"))
    count_answers = Column(BIGINT, nullable=False, default=0)

    user = relationship(User, foreign_keys=[user_id])


class TelegramMessage(BaseMixin, Base):
    __tablename__ = 'telegram_message'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    forWhom = Column(String, default=UserRole.USER)
    countMessage = Column(Integer)
    message = Column(VARCHAR(length=4096), nullable=True)


class MiniCourse(BaseMixin, Base):
    __tablename__ = 'minicourses'

    id = Column(Integer, primary_key=True)
    user_id = Column(BIGINT, ForeignKey("users.id", onupdate="CASCADE", ondelete="RESTRICT"))
    date_start = Column(DateTime, default=datetime.now)
    day_one = Column(Boolean, nullable=True, default=False)
    day_two = Column(Boolean, nullable=True, default=False)
    day_three = Column(Boolean, nullable=True, default=False)
    day_four = Column(Boolean, nullable=True, default=False)
    day_five = Column(Boolean, nullable=True, default=False)
    day_six = Column(Boolean, nullable=True, default=False)
    day_seven = Column(Boolean, nullable=True, default=False)
    day_eight = Column(Boolean, nullable=True, default=False)
    finish = Column(Boolean, nullable=True, default=False)

    user = relationship(User, back_populates="mini_courses")


class SavingCalculation(BaseMixin, Base):
    __tablename__ = 'saving_calculations'

    id = Column(Integer, primary_key=True)
    men = Column(VARCHAR(32), default=0)
    women = Column(VARCHAR(32), default=0)
    children_under_5_yo = Column(VARCHAR(32), default=0)
    children_after_5_yo = Column(VARCHAR(32), default=0)

    user_id = Column(BIGINT, ForeignKey("users.id"))

    user = relationship(User, back_populates="calculations")


class Webinar(BaseMixin, Base):
    __tablename__ = "webinars"

    id = Column(Integer, primary_key=True)
    date_start = Column(DateTime)
