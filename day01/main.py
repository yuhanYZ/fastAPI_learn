from datetime import date

from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

import shutil
from pathlib import Path
from typing import Annotated

from fastapi import Depends, File, Form, HTTPException, Request, UploadFile
from pydantic import EmailStr

from routers.shop import shop
from routers.user import user
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import schemas
import models

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
app.include_router(shop,prefix="/shop",tags=["购物中心接口"])
app.include_router(user,prefix="/user",tags=["用户中心接口"])

#创建学生的接口
@app.post("/students",response_model=schemas.StudentOut)
def create_student(
        student: schemas.StudentCreate,
        db: Session = Depends(get_db),
):
    db_student = models.Student(
        name=student.name,
        age=student.age,
        class_name=student.class_name,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student

#查询学生的接口
@app.get("/students",response_model=list[schemas.StudentOut])
async def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students

@app.get("/students/{student_id}",response_model=schemas.StudentOut)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()

    if student is None:
        raise HTTPException(status_code=404, detail="student not found")
    return student
@app.get("/")
async def root():
    return {"message": "Hello yuan"}


# 路径参数：固定路径必须写在带参数的路径前面
@app.get("/user/me")
async def read_me():
    return {"username": "the current user"}


@app.get("/user/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}


# 查询参数：不在路径里的函数参数；有默认值就是可选
@app.get("/jobs/{kd}")
async def search_jobs(kd: str, city: str | None = None, xl: str | None = None):
    return {"kd": kd, "city": city, "xl": xl}


# 请求体：继承 BaseModel
class User(BaseModel):
    name: str = "root"
    age: int = Field(default=1, gt=0, lt=100)
    birth: date | None = None
    friends: list[int] = []

    @field_validator("name")
    @classmethod
    def name_must_alpha(cls, v: str) -> str:
        if not v.isalpha():
            raise ValueError("name must be alpha")
        return v


@app.post("/users")
async def create_user(user: User):
    return user

@app.post("/login")
async def login(
    username: Annotated[str, Form(min_length=3, max_length=16)],
    password: Annotated[str, Form(min_length=8)],
    ):
    return {"username":username}

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()              # 读出文件的全部内容（bytes）
    with open(file.filename, "wb") as f:     # "wb" = 以二进制方式写入
        f.write(content)
    return {"filename": file.filename, "size": len(content)}

# 3. Request 对象：直接拿到请求本身的信息
@app.get("/whoami")
async def whoami(request: Request):
    return{
        "url":str(request.url),
        "ip": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
    }

# 4. response_model：控制"返回什么字段"
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserOut(BaseModel):
    username: str
    email: EmailStr

@app.post("/register", response_model=UserOut)
async def register(user: UserIn):
    return user          # 返回的是 UserIn，但响应里 password 会被过滤掉