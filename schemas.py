from pydantic import BaseModel  
from typing import Optional 

class SignUp(BaseModel):
    id : Optional[int]
    username : str
    email : str
    password : str
    is_staff : Optional[bool] 
    is_active : Optional[bool] 

    class Config:
        orm_mode = True 
        schema_extra = {
            'example': {
                'username': 'radin8',
                'email': 'raadin.dev@gmail.com',
                'password': 'radin1234',
                'is_staff':False,
                'is_active':True
            }
        }

# Getting a secret key 
class Setting(BaseModel):
    authjwt_secret_key: str = '1ba56a71c8907be23b02a307ebf03a5cf26c6c8df41f772a53d8429d71ffa317' 

class Login(BaseModel):
    username: str 
    password: str

class OrderModel(BaseModel):
    id : Optional[int]
    quantity : int 
    order_status : Optional[str] = 'PENDING' 
    pizza_size : Optional[str] = 'SMALL'
    user_id : Optional[int]

    class Config:
        orm_mode = True 
        schema_extra = {
            'example':{
                'quantity': 2, 
                'pizza_size':'SMALL'
            }
        }
