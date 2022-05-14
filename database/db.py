from sqlalchemy import Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR, '.env')

DB_ENGINE = ${DB_ENGINE}
DB_USER = ${DB_USER}
DB_PASSWORD = ${DB_PASSWORD}
DB_HOST = ${DB_HOST}
DB_DATABASE = ${DB_DATABASE}

Engine = create_engine(f'{DB_ENGINE}+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}')

Base = declarative_base()

SessionLocal = sessionmaker(engine=Engine)

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

