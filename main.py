from fastapi import FastAPI
from routers import user, user_db, product, jwt_auth_autentication, simple_autentication
from fastapi.staticfiles import StaticFiles

app = FastAPI() 

app.include_router(user.router)
app.include_router(user_db.router)
app.include_router(product.router)
app.include_router(jwt_auth_autentication.router)
app.include_router(simple_autentication.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root():
    return {"Hello": "World"}