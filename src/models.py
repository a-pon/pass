import enum
from datetime import datetime, UTC

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Status(str, enum.Enum):
    new = 'new'
    pending = 'pending'
    accepted = 'accepted'
    rejected = 'rejected'


class Level(str, enum.Enum):
    one_a = '1А'
    one_b = '1Б'
    two_a = '2А'
    two_b = '2Б'
    three_a = '3А'
    three_b = '3Б'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False, unique=True)
    phone = Column(String(32))


class PerevalAdded(Base):
    __tablename__ = 'pereval_added'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    status = Column(Enum(Status), default=Status.new)
    user_id = Column(Integer, ForeignKey('users.id'))
    coord_id = Column(Integer, ForeignKey('coords.id'))
    beauty_title = Column(String(128))
    title = Column(String(128), nullable=False)
    other_titles = Column(String(256))
    connect = Column(String(128))
    add_time = Column(TIMESTAMP, default=lambda: datetime.now(UTC))
    level_winter = Column(Enum(Level), nullable=True)
    level_spring = Column(Enum(Level), nullable=True)
    level_summer = Column(Enum(Level), nullable=True)
    level_autumn = Column(Enum(Level), nullable=True)

    user = relationship('User')
    coords = relationship('Coords')
    images = relationship('PerevalImage', back_populates='pereval', cascade='all, delete-orphan')


class Coords(Base):
    __tablename__ = 'coords'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    latitude = Column(Float)
    longitude = Column(Float)
    height = Column(Integer)


class PerevalImage(Base):
    __tablename__ = 'pereval_images'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    pereval_id = Column(Integer, ForeignKey('pereval_added.id'))
    image_url = Column(String(256))

    pereval = relationship('PerevalAdded', back_populates='images')
