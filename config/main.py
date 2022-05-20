from fastapi  import FastAPI
from blog     import main as mainblog, models as blog_model
from accounts import main as mainaccounts, models as account_models


app = FastAPI()
app.include_router(mainaccounts.router)
app.include_router(mainblog.router)

