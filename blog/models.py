from   accounts.models  import UserModel
from   sqlalchemy.orm  import relationship, backref
import sqlalchemy      as sa
from   sqlalchemy      import func
from   sqlalchemy.sql  import expression
from   config.settings import Base, Engine



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
    image_path    = sa.Column(sa.String())
    created       = sa.Column(sa.DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated       = sa.Column(sa.DateTime(timezone=True), onupdate=func.now(), nullable=True)
    user_id       = sa.Column(sa.Integer(), sa.ForeignKey('Users.id'))
    user          = relationship('UserModel', backref=backref('blogs', cascade="all,delete-orphan"))
    

class CommentBlogModel(Base):
    __tablename__ = 'CommentsBlog'
    id            = sa.Column(sa.Integer(), primary_key=True, index=True)
    name          = sa.Column(sa.String(250))
    email         = sa.Column(sa.String(250))
    messages      = sa.Column(sa.Text())
    blog_id       = sa.Column(sa.Integer(), sa.ForeignKey('Blogs.id'))
    blog          = relationship('BlogModel', backref=backref('comments', cascade='all,delete-orphan'))

Base.metadata.create_all(Engine)