from config.db import Base, Engine
from sqlalchemy import Column, Integer, String, Boolean, Text

class BlogModel(Base):
    __tablename__ = 'Blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    phone_number = Column(Integer)
    publish = Boolean(False)
    tags = Column(String)
    meta_data = Column(Text)
    
    
Base.metadata.create_all(Engine)