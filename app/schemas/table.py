from pydantic import BaseModel
from typing import Optional


class TableBase(BaseModel):
    name: str
    seats: int
    location: str


class TableCreate(TableBase):
    pass


class TableUpdate(BaseModel):
    number: Optional[int] = None
    seats: Optional[int] = None


class TableRead(TableBase):
    id: int

    class Config:
        orm_mode = True
