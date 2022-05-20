from   config.db       import Base, Engine
from   sqlalchemy.orm  import relationship
from   accounts.models import UserModel
from   datetime        import datetime
import sqlalchemy      as sa


class BlogModel(Base):
    __tablename__ = 'Blogs'
    id            = sa.Column(sa.Integer(), primary_key=True, index=True)
    title         = sa.Column(sa.String(255))
    description   = sa.Column(sa.Text())
    phone_number  = sa.Column(sa.Integer())
    publish       = sa.Column(sa.Boolean(), default=False)
    tags          = sa.Column(sa.String(255))
    status        = sa.Column(sa.String())
    image         = sa.Column(sa.String())
    created       = sa.Column(sa.DateTime(timezone=True), nullable=False)
    updated       = sa.Column(sa.DateTime(timezone=True), onupdate=datetime.utcnow, nullable=False)
    user_id       = sa.Column(sa.Integer(), sa.ForeignKey('Users.id'))
    user          = relationship('UserModel', backref='blogs', cascade='save-update')
    
    
class CommentBlogModel(Base):
    __tablename__ = 'CommentsBlog'
    id            = sa.Column(sa.Integer(), primary_key=True, index=True)
    name          = sa.Column(sa.String(250))
    email         = sa.Column(sa.String(250))
    messages      = sa.Column(sa.Text())
    blog_id       = sa.Column(sa.Integer(), sa.ForeignKey('Blogs.id'))
    blog          = relationship('BlogModel', backref='comments', cascade='delete')


Base.metadata.create_all(Engine)