from pydantic import BaseModel, EmailStr

class custoemr_request_Add(BaseModel):
    name: str
    email: EmailStr
    address: str
    phone_number: str  # Changed to string for better compatibility
    whatsapp_number:str
    is_delete : bool = False

class custoemr_request_responce(BaseModel):
    id: int
    name: str
    email: EmailStr
    address: str
    phone_number: str  # Changed to string for better compatibility
    whatsapp_number:str
    is_delete : bool = False