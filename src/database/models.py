# src/database/models.py
from sqlalchemy import Column, Integer, String, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass

class Admin(Base):
    __tablename__ = 'admins'
    user_id = Column(BigInteger, primary_key=True)


class Channel(Base):
    __tablename__ = 'channels'
    channel_id = Column(BigInteger, primary_key=True)
    channel_name = Column(Text)
    adder_user_id = Column(BigInteger, nullable=False)

class AuthorizedUser(Base):
    __tablename__ = 'authorized_users'
    id = Column(Integer, primary_key=True)
    tg_user_id = Column(BigInteger)
    platform_user_id = Column(Integer)
    chat_id = Column(BigInteger)
    institutionId = Column(Integer)
    