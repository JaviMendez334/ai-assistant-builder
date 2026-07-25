from pydantic import BaseModel, EmailStr


class User(BaseModel):
    nombre: str


class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}
    
