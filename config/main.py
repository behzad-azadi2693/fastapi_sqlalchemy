from fastapi  import FastAPI
from blog     import main as mainblog
from accounts import main as mainaccounts
from . import models


app = FastAPI()
app.include_router(mainaccounts.router)
app.include_router(mainblog.router)

