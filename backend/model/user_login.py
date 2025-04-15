from sqlalchemy import Column, Integer, String,Boolean
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String(255), unique=True, index=True)  # Added length for email
    password = Column(String)
    role = Column(String, default="user")
    is_deleted = Column(Boolean,default=False)
