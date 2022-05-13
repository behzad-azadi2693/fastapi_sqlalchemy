from fastapi import FastAPI
from blog import main
from database import models
from database.db import Engine

app = FastAPI()
app.include_router(main.router)
models.Base.metadata.create_all(Engine)

@app.get('/', tags=['v1'])
def index(response_descriptions='this first page'):
    """
    project for **learning**
    """
    return "hello world"

