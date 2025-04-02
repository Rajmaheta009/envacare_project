from requests import Session
from sqlalchemy import Column, Integer, String,text,Boolean
from database import Base

# Quotation Model
class Parent_Parameter(Base):
    __tablename__ = "parent_parameter"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    is_delete = Column(Boolean, default=False)
