from fastapi import APIRouter
from utils.jwt_manager import create_token
from schemas import User

user_router = APIRouter()

@user_router.post('/login', tags=['auth'], status_code=200)
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return token
    return user
