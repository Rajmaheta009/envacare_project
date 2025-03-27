from sqlalchemy import Column, Integer, String, Boolean, func, DateTime
from database import Base


class Customer_request(Base):
    __tablename__ = "customer_info"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String(255), unique=True, index=True)  # Added length for email
    address = Column(String)
    phone_number = Column(String)  # Changed to String for phone number
    whatsapp_number = Column(String)  # Changed to String for phone number
    is_delete = Column(Boolean, default=False)  # Changed to Boolean for clarity
    created_at = Column(DateTime, server_default=func.now(), onupdate=None)
