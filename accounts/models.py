from   sqlalchemy.orm  import relationship, backref
import sqlalchemy      as sa
from   config.settings import Base, Engine


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
    fullname      = sa.Column(sa.String(250))
    title         = sa.Column(sa.String(120))
    description   = sa.Column(sa.Text())
    user_id       = sa.Column(sa.Integer(), sa.ForeignKey('Users.id'))
    user          = relationship('UserModel', backref=backref('profile', cascade='all,delete-orphan'), uselist=False)


class ImageModel(Base):
    __tablename__ = 'Images'
    id            = sa.Column(sa.Integer(), primary_key=True, index=True)
    image         = sa.Column(sa.String())
    user_id       = sa.Column(sa.Integer(), sa.ForeignKey('Users.id'))
    user          = relationship('UserModel', backref=backref('image', cascade='all,delete-orphan'), uselist=False)


Base.metadata.create_all(Engine)