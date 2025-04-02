from pydantic import BaseModel

class ParameterCreate(BaseModel):
    parent_id :int
    name:str
    price: float
    min_range :float
    max_range : float
    protocol : str


class ParameterUpdate(BaseModel):
    parent_id : int
    name: str
    price: float
    min_range : float
    max_range : float
    protocol : str
