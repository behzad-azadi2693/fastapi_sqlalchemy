from fastapi import FastAPI
from blog import main as mainblog
from accounts import main as mainaccounts
from database import models
from database.db import Engine

app = FastAPI()
app.include_router(mainaccounts.router)
app.include_router(mainblog.router)
models.Base.metadata.create_all(Engine)

