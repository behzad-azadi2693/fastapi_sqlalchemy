Generic single-database configuration.

change in directory alembic file .env[
    from config.models import Base
    from config.db import BASE_DIR
    import os
    from dotenv import load_dotenv

    load_dotenv(os.path.join(BASE_DIR, ".env"))
    target_metadata = [Base.metadata] 
    config.set_main_option("sqlalchemy.url", os.getenv("DB_ENGINE"))
]

alembic init alembic
alembic revision --autogenerate -m "<ypur_commit>"
alembic upgrade head