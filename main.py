from fastapi import FastAPI 
from auth_routes import auth_router 
from order_routes import order_router 
from fastapi_jwt_auth import AuthJWT 
from schemas import Setting

app = FastAPI()

@AuthJWT.load_config 
def get_config():
    return Setting()

app.include_router(auth_router)
app.include_router(order_router)