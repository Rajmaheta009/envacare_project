from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from modal.quotation import Quotation
from schema.quotation import QuotationCreate

router = APIRouter()

@router.post("/", response_model=QuotationCreate)
def create_quotation(quotation: QuotationCreate, db: Session = Depends(get_db)):
    new_quotation = Quotation(**quotation.dict())
    db.add(new_quotation)
    db.commit()
    db.refresh(new_quotation)
    return new_quotation

@router.get("/")
def get_quotations(db: Session = Depends(get_db)):
    return db.query(Quotation).all()

