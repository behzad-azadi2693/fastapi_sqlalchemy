from fastapi           import FastAPI, Query, Body
from fastapi.responses import FileResponse
from blog              import router as routerBlog, models as blogmodels
from accounts          import router as routerAccounts, models as accountsmodels


app = FastAPI()
app.include_router(routerAccounts.router)
app.include_router(routerBlog.router)


@app.get('/image/response/')
async def image_response(url:str):
    
    return FileResponse(url)
