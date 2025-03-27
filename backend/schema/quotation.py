from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


# Quotation Schema
class QuotationCreate(BaseModel):
    order_id: int
    pdf_url:str