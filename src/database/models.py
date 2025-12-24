# src/database/models.py
from sqlalchemy import Column, Integer, String, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass

class Admin(Base):
    __tablename__ = 'admins'
    user_id = Column(BigInteger, primary_key=True)


class Institution(Base):
    __tablename__ = 'institutions'
    id = Column(Integer, primary_key=True)
    institutionName = Column(Text, nullable=False)
    channels = relationship("Channel", back_populates="institution")

class Channel(Base):
    __tablename__ = 'channels'
    channel_id = Column(BigInteger, primary_key=True)
    channel_name = Column(Text)
    institutionId = Column(Integer, ForeignKey('institutions.id') ,nullable=False)
    adder_user_id = Column(BigInteger, nullable=False)
    institution = relationship("Institution", back_populates="channels")
    