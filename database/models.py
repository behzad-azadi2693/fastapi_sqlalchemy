from .db import Base
from sqlalchemy import Column, Integer, String, Boolean

class DbUser(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(250), unique=True)
    email = Column(String(250))
    password = Column(String(100))
    is_active = Column(Boolean(True))
    is_admin = Column(Boolean(False))
    is_superuser = Column(Boolean(False))