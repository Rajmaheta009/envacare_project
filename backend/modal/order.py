from requests import Session
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, text
from datetime import datetime
from database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer_info.id"), nullable=False)
    order_req_comment = Column(String(255))
    order_req_doc = Column(String(255))
    status = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

def get_next_id(db: Session):
    result = db.execute(text("SELECT nextval(pg_get_serial_sequence('order', 'id'))"))
    return result.scalar()