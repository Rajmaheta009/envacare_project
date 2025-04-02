from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from modal.parent_parameter import Parent_Parameter
from schema.parent_parameter import Parent_ParameterCreate,Parent_ParameterUpdate

router = APIRouter()

@router.post("/", status_code=200)
async def create_parent_parameter(parent_parameter: Parent_ParameterCreate, db: Session = Depends(get_db)):
    try:
        db_parameter = Parent_Parameter(**parent_parameter.dict())
        db.add(db_parameter)
        db.commit()
        db.refresh(db_parameter)
        return db_parameter
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating parent parameter: {str(e)}")

@router.get("/", status_code=200)
def get_all_parent_parameter(db: Session = Depends(get_db)):
    try:
        parameters = db.query(Parent_Parameter).filter(Parent_Parameter.is_delete == False).all()
        return [{"id": c.id, "name": c.name} for c in parameters]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching parent parameters: {str(e)}")

@router.put("/{parent_parameter_id}", status_code=200)
def update_parent_parameter(parent_parameter_id: int, parent_parameter: Parent_ParameterUpdate, db: Session = Depends(get_db)):
    db_parameter = db.query(Parent_Parameter).filter(Parent_Parameter.id == parent_parameter_id).first()

    if db_parameter:
        if db_parameter.name != parent_parameter.name:
            db_parameter.name = parent_parameter.name
            db.commit()
            db.refresh(db_parameter)
            return db_parameter
        else:
            raise HTTPException(status_code=400, detail="New parameter value is the same as the current one.")
    else:
        raise HTTPException(status_code=404, detail="Parent parameter not found")

@router.delete("/{p_id}", status_code=200)
def delete_parameter(p_id: int, db: Session = Depends(get_db)):
    db_parameter = db.query(Parent_Parameter).filter(Parent_Parameter.id == p_id).first()

    if db_parameter:
        db_parameter.is_delete = True
        db.commit()
        return {"message": f"Parent parameter with id {p_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Parent parameter not found")
