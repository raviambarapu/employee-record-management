from pydantic import BaseModel, EmailStr, Field


class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    department: str = Field(..., min_length=2, max_length=100)
    salary: float = Field(..., gt=0)


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    salary: float

    class Config:
        from_attributes = True