from   sqlalchemy.orm  import relationship
import sqlalchemy      as sa
from   sqlalchemy      import func
from   sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import expression
from .settings import Engine

Base = declarative_base()
metadata = Base.metadata


#THIS FOR DESIGN MODELS FOR ACCOUNTS APP
class UserModel(Base):
    __tablename__ = 'Users'
    id            = sa.Column(sa.Integer(), primary_key=True, index=True)
    username      = sa.Column(sa.String(250), unique=True)
    email         = sa.Column(sa.String(250))
    password      = sa.Column(sa.String(100))
    is_active     = sa.Column(sa.Boolean(), default=True)
    is_admin      = sa.Column(sa.Boolean(), default=False)
    is_superuser  = sa.Column(sa.Boolean(), default=False)


class ProfileModel(Base):
    __tablename__ = 'Profile'
    id            = sa.Column(sa.Integer(), primary_key=True, index=True)
    fulname       = sa.Column(sa.String(250))
    title         = sa.Column(sa.String(120))
    description   = sa.Column(sa.Text())
    user_id       = sa.Column(sa.Integer(), sa.ForeignKey('Users.id'))
    user          = relationship('UserModel', backref='profile', uselist=False, cascade='delete')


class ImageModel(Base):
    __tablename__ = 'ProfileImage'
    id            = sa.Column(sa.Integer(), primary_key=True, index=True)
    image         = sa.Column(sa.String())
    profile_id    = sa.Column(sa.Integer(), sa.ForeignKey('Profile.id'))
    profile       = relationship('ProfileModel', backref='images', cascade='all, delete')

#THIS FOR DESIGN MODELS FOR BLOG APP
class BlogModel(Base):
    __tablename__ = 'Blogs'
    id            = sa.Column(sa.Integer(), primary_key=True, index=True)
    title         = sa.Column(sa.String(255))
    description   = sa.Column(sa.Text())
    phone_number  = sa.Column(sa.Integer())
    publish       = sa.Column(sa.Boolean(), server_default=expression.false(), nullable=True)
    tags          = sa.Column(sa.String(255))
    status        = sa.Column(sa.String())
    image         = sa.Column(sa.String())
    created       = sa.Column(sa.DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated       = sa.Column(sa.DateTime(timezone=True), onupdate=func.now(), nullable=True)
    user_id       = sa.Column(sa.Integer(), sa.ForeignKey('Users.id'))
    user          = relationship('UserModel', backref='blogs')
    

class CommentBlogModel(Base):
    __tablename__ = 'CommentsBlog'
    id            = sa.Column(sa.Integer(), primary_key=True, index=True)
    name          = sa.Column(sa.String(250))
    email         = sa.Column(sa.String(250))
    messages      = sa.Column(sa.Text())
    blog_id       = sa.Column(sa.Integer(), sa.ForeignKey('Blogs.id'))
    blog          = relationship('BlogModel', backref='comments', cascade='delete')

Base.metadata.create_all(Engine)