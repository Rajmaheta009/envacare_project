from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from modal.parameter import Parameter
from schema.parameter import ParameterCreate

router = APIRouter()

@router.post("/", status_code=200)
async def create_parameter(parameter: ParameterCreate, db: Session = Depends(get_db)):
    db_parameter = Parameter(**parameter.dict())
    db.add(db_parameter)
    db.commit()
    db.refresh(db_parameter)
    return db_parameter

@router.get("/", status_code=200)
def get_all_parameters(db: Session = Depends(get_db)):
    parameters = db.query(Parameter).filter(Parameter.is_delete == False).all()
    return [{"id": p.id, "parent_id": p.parent_id, "name": p.name, "price": p.price,
             "min_range": p.min_range, "max_range": p.max_range,"protocol":p.protocol} for p in parameters]

@router.put("/{parameter_id}", status_code=200)
def update_parameter(parameter_id:int,parameter: ParameterCreate, db: Session = Depends(get_db)):
    # Retrieve the existing parameter record by its ID
    db_parameter = db.query(Parameter).filter(Parameter.id == parameter_id).first()

    if db_parameter:
        # Update the existing record's fields with new values
        for key, value in parameter.dict().items():
            setattr(db_parameter, key, value)
        db.commit()
        db.refresh(db_parameter)
        return db_parameter
    else:
        return {"error": "Parameter not found"}

@router.delete("/", status_code=200)
def delete_parameter(p_id:int,db:Session = Depends(get_db)):
    db_parameter = db.query(Parameter).filter(Parameter.id == p_id).first()

    if db_parameter:
        db_parameter.is_delete = True
    else:
        raise HTTPException(status_code=404, detail="Customer_request not found")
    db.commit()
    return {"message": "Customer_request deleted successfully"}