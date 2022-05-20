from config.db import Base, Engine
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship, backref

class UserModel(Base):
    __tablename__ = 'Users'
    id = Column(Integer(), primary_key=True, index=True)
    username = Column(String(250), unique=True)
    email = Column(String(250))
    password = Column(String(100))
    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)

class ProfileModel(Base):
    __tablename__ = 'Profile'
    id = Column(Integer(), primary_key=True, index=True)
    fulname = Column(String(250))
    title = Column(String(120))
    description = Column(Text())
    user_id = Column(Integer(), ForeignKey('Users.id'))
    user = relationship('UserModel', backref='profile', uselist=False, cascade='delete')

class ImageModel(Base):
    __tablename__ = 'ProfileImage'
    id = Column(Integer(), primary_key=True, index=True)
    image = Column(String())
    profile_id = Column(Integer(), ForeignKey('Profile.id'))
    profile = relationship('ProfileModel', backref='images', cascade='all, delete')

Base.metadata.create_all(Engine)