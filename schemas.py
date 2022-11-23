from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    pin: Optional[str]
    lat: Optional[float]
    long: Optional[float]
    email: Optional[str]
    label: Optional[str]

    class Config:
        orm_mode = True
