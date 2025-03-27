from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from modal.customer_request import Customer_request
from schema.customer_request import custoemr_request_Add,custoemr_request_responce
from typing import List

router = APIRouter()

@router.post("/", response_model=custoemr_request_responce)
def create_customer(customer: custoemr_request_Add, db: Session = Depends(get_db)):
    db_customer = Customer_request(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/", response_model=List[custoemr_request_responce])
def get_all_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer_request).filter(Customer_request.is_delete == False).all()
    return customers

@router.get("/{customer_id}", response_model=custoemr_request_responce)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer_request).filter(Customer_request.id == customer_id, Customer_request.is_delete == False).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer_request not found")
    return customer

@router.put("/{customer_id}", response_model=custoemr_request_responce)
def update_customer(customer_id: int, customer: custoemr_request_Add, db: Session = Depends(get_db)):
    db_customer = db.query(Customer_request).filter(Customer_request.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer_request not found")
    for key, value in customer.dict(exclude_unset=True).items():
        setattr(db_customer, key, value)
    db.commit()
    return db_customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer_request).filter(Customer_request.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer_request not found")
    customer.is_delete = True
    db.commit()
    return {"message": "Customer_request deleted successfully"}
