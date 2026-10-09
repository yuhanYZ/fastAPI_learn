from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    age: int
    class_name: str | None = None


class StudentOut(BaseModel):
    id: int
    name: str
    age: int
    class_name: str | None = None