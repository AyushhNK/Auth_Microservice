from pydantic import BaseModel, EmailStr, Field

class UserCreateSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, description="The user's username")
    email: EmailStr = Field(..., description="The user's email address")
    password1: str = Field(..., min_length=8, description="The user's password")
    password2: str = Field(..., min_length=8, description="Password confirmation")