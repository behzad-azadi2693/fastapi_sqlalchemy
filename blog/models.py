from config.db import Base, Engine
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from accounts.models import UserModel


class BlogModel(Base):
    __tablename__ = 'Blogs'
    id = Column(Integer(), primary_key=True, index=True)
    title = Column(String())
    description = Column(Text())
    phone_number = Column(Integer())
    publish = Column(Boolean(), default=False)
    tags = Column(String())
    status = Column(String())
    image = Column(String())
    user_id = Column(Integer(), ForeignKey('Users.id'))
    user = relationship('UserModel', backref='blogs', cascade='save-update')
    
    
class CommentBlogModel(Base):
    __tablename__ = 'CommentsBlog'
    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String(250))
    email = Column(String(250))
    messages = Column(Text())
    blog_id = Column(Integer(), ForeignKey('Blogs.id'))
    blog = relationship('BlogModel', backref='comments', cascade='delete')


Base.metadata.create_all(Engine)