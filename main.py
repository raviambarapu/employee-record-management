from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import crud

from database import engine, get_db
from schemas import EmployeeCreate, EmployeeResponse


# Create database tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Employee Management API",
    description="FastAPI CRUD application with PostgreSQL and SQLAlchemy",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Employee Management API is running"
    }


# CREATE
@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=201
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    existing_employee = db.query(models.Employee).filter(
        models.Employee.email == employee.email
    ).first()

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return crud.create_employee(db, employee)


# READ ALL
@app.get(
    "/employees",
    response_model=list[EmployeeResponse]
)
def get_employees(
    db: Session = Depends(get_db)
):
    return crud.get_employees(db)


# READ ONE
@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = crud.get_employee(db, employee_id)

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# UPDATE
@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    updated_employee = crud.update_employee(
        db,
        employee_id,
        employee
    )

    if not updated_employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return updated_employee


# DELETE
@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    deleted_employee = crud.delete_employee(
        db,
        employee_id
    )

    if not deleted_employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee deleted successfully"
    }