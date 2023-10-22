from datetime import datetime
from enum import Enum
from typing import List, Optional

import fastapi
from fastapi import Depends
from fastapi_users import FastAPIUsers
from pydantic import BaseModel, Field

from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

app=fastapi.FastAPI(
    title='Trading App'
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.get("/unprotected-route")
def protected_route():
    return f"Hello, anonym!"

#fake_users=[
#    {'id':1,'role':'admin','name':'Bob'},
#    {'id':2,'role':'investor','name':'John','degree':[
#        {'id':1,'created_at':'2020-01-01T00:00:00','type_degree':'newbie'}
#    ]},
#    {'id':3,'role':'trader','name':'Matt','degree':[
#        {'id':1,'created_at':'2020-01-01T00:00:00','type_degree':'expert'}
#    ]}
#]
#class DegreeType(Enum):
#    newbie='newbie'
#    expert='expert'
#class Degree(BaseModel):
#    id: int
#    created_at: datetime
#    type_degree: DegreeType
#class User(BaseModel):
#    id: int
#    role:str
#    name:str
#    degree: Optional[List[Degree]] = []
#
#
#@app.get('/users/{user_id}',response_model=List[User])
#def index(user_id:int):
#    return [user for user in fake_users if user.get('id')==user_id]
#
#
#
#fake_trades=[
#    {'id':1,'user_id':1,'currency':'BTC','side':'buy','price':123,'amount':2.12},
#    {'id':2,'user_id':1,'currency':'BTC','side':'sell','price':125,'amount':2.12},
#]
#
#class Trade(BaseModel):
#    id:int
#    user_id:int
#    currency:str = Field(max_length=5)
#    side:str
#    price:float = Field(ge=0)
#    amount:float
#@app.post('/trades')
#def add_trades(trades:List[Trade]):
#    fake_trades.extend(trades)
#    return {'status':200,'data':fake_trades}
#
#
#
#
#@app.get('/trades')
#def get_trades(limit:int=1,offset:int=0):
#    return fake_trades[offset:][:limit]
#
#
#
#fake_users2=[
#    {'id':1,'role':'admin','name':'Bob'},
#    {'id':2,'role':'investor','name':'John'},
#    {'id':3,'role':'trader','name':'Matt'}
#]
#
#
#@app.post('/users/{user_id}')
#def change_user_name(user_id:int,new_name:str):
#    current_user=list(filter(lambda user:user.get('id')==user_id,fake_users2))
#    try:
#        current_user[0]['name']=new_name
#        return {'status': 200, 'data': current_user}
#    except:
#        return {'status': 500, 'data': 'такого пользователя нет'}


