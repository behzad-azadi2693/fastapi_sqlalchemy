from fastapi  import FastAPI
from blog     import router as routerBlog
from accounts import router as routerAccounts
from . import models


app = FastAPI()
app.include_router(routerAccounts.router)
app.include_router(routerBlog.router)

