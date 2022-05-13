from sqlalchemy import Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Engine = create_engine('postgresql+psycopg2://postgres_user:postgres_password@localhost/blog_db')

Base = declarative_base()

SessionLocal = sessionmaker(engine=Engine)

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

