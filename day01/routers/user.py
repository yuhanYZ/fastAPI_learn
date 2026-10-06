from fastapi import APIRouter

user = APIRouter()

@user.get("/login", summary="登录接口",description="主要用来登录")
async def user_login():
    return {"user": "login"}

@user.get("/register",summary="注册接口",description="主要用来注册用户")
async def user_register():
    return {"user": "register"}