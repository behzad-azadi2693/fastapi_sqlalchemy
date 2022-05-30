from fastapi  import FastAPI
from blog     import router as routerBlog, models as blogmodels
from accounts import router as routerAccounts, models as accountsmodels


app = FastAPI()
app.include_router(routerAccounts.router)
app.include_router(routerBlog.router)

