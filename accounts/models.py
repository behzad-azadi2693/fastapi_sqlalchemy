from  config.db      import Base, Engine
from  sqlalchemy.orm import relationship, backref
import sqlalchemy    as sa


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


Base.metadata.create_all(Engine)