from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from database import Base
# Quotation Model
class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    pdf_url= Column(String)
    created_at = Column(DateTime, server_default=func.now())
