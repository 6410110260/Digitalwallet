from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from sqlmodel import Relationship, SQLModel, Field
from . import merchants

class BaseItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    merchant_id: int

class CreatedItem(BaseItem):
    pass

class UpdatedItem(BaseItem):
    pass

class Item(BaseItem):
    id: int

class DBItem(SQLModel, Item, table=True):
    # Correctly define the primary key with default=None
    id: int = Field(default=None, primary_key=True)
    # Properly set foreign key reference
    merchant_id: int = Field(default=None, foreign_key="dbmerchant.id")
    # Use proper type hints for relationship
    merchant: merchants.DBMerchant | None = Relationship(back_populates="items")

class ItemList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    items: List[Item]
    page: int
    page_size: int
    size_per_page: int