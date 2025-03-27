from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class OrderBase(BaseModel):
    customer_id: int
    order_req_comment: Optional[str] = Field(None, max_length=255)
    order_req_doc: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, max_length=255)

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    order_req_comment: Optional[str] = Field(None, max_length=255)
    order_req_doc: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, max_length=255)

class OrderOut(OrderBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
