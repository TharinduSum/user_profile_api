from pydantic import BaseModel
from typing import Optional

class AddressBase(BaseModel):
    address_line_one: str
    address_line_two: Optional[str] = None
    city: str
    country: str

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    occupation: str
    address: AddressBase

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    occupation: Optional[str] = None
    address: Optional[AddressBase] = None

class AddressResponse(AddressBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    occupation: str
    profile_picture: Optional[str]
    address: Optional[AddressResponse]

    class Config:
        orm_mode = True

#dtaValidtnPydentic