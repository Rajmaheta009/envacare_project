from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from modal.user_login import User
from schema.user_login import UserLogin

router = APIRouter()

@router.post("/", status_code=200)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if db_user.is_deleted:
        raise HTTPException(status_code=404, detail="User is deleted")
    if user.password != db_user.password:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    return {
        "status": "success",
        "id": db_user.id,
        "username": db_user.name,
        "email": db_user.email,
        "role": db_user.role
    }
