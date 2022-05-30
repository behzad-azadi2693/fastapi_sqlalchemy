from   sqlalchemy                 import create_engine
from   sqlalchemy.orm             import sessionmaker, Session
from   dotenv                     import load_dotenv
from   pathlib                    import Path
import os
from   sqlalchemy.ext.declarative import declarative_base

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR/'.env'))

Engine = create_engine(os.getenv('DB_ENGINE'))

SessionLocal = sessionmaker(bind=Engine, autocommit=False, autoflush=False)

SECRET_KEY = os.getenv('SECRET_KEY')

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

Base = declarative_base()
metadata = Base.metadata

try:
    os.mkdir(os.path.join(BASE_DIR, 'media'))
    
    print('directory for save manage is created')
except:
    print('directory is exits')


