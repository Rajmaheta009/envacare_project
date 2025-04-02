from pydantic import BaseModel

class Parent_ParameterCreate(BaseModel):
    name: str


class Parent_ParameterUpdate(BaseModel):
    name: str