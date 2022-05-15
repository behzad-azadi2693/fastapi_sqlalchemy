from sqlalchemy import Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR/'.env')

db = f"{os.getenv('DB_ENGINE')}+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:5432/{os.getenv('DB_NAME')}"
Engine = create_engine(db)

Base = declarative_base()

SessionLocal = sessionmaker(bind=Engine, autocommit=False, autoflush=False)

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

