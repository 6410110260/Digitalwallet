from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel,Relationship
from .users import *
from .wallets import *

class BaseCustomer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None
    tax_id: str | None = None
    
class CreatedCustomer(BaseCustomer):
    pass

class UpdatedCustomer(BaseCustomer):
    pass

class Customer(BaseCustomer):
    id: int
    user_id: int
    
class DBCustomer(BaseCustomer, SQLModel, table=True):
    __tablename__ = "customers"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    user_id: int = Field(default=None, foreign_key="users.id")
    user: DBUser | None = Relationship(back_populates="customer")

    #wallets: list["DBWallet"] = Relationship(back_populates="customer")
    

class CustomerList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    customers: list[Customer]
    page: int
    page_size: int
    size_per_page: int