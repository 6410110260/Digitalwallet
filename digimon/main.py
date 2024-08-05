from fastapi import FastAPI, HTTPException

from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlmodel import Field, SQLModel, create_engine, Session, select


class BaseMerchant(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    description: str
    merchant_type: str
    location: str
    tax_id: str | None = None

class BaseWallet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    owner: str
    balance: float


class BaseTransaction(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sender: str
    receiver: str
    amount: float

class BaseItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str | None = None
    price: float = 0.12
    tax: float | None = None
    merchant_id: int | None



class CreatedItem(BaseItem):
    pass


class UpdatedItem(BaseItem):
    pass

class CreatedMerchant(BaseMerchant):
    pass

class UpdateMerchant(BaseMerchant):
    pass

class CreatedTransaction(BaseTransaction):
    pass

class CreatedWallet(BaseWallet):
    pass

class UpdateWallet(BaseWallet):
    pass

class Merchant(BaseMerchant):
    id: int

class Wallet(BaseWallet):
    id: int

class Transaction(BaseTransaction):
    id: int

class Item(BaseItem):
    id: int
    merchant_id: int



class ItemList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    items: list[Item]
    page: int
    page_size: int
    size_per_page: int

class Merchant_list(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    merchants: list[Merchant]
    page: int
    page_size: int
    size_per_page: int

class Transaction_list(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transactions: list[Transaction]
    page: int
    page_size: int
    size_per_page: int

class Wallet_list(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    wallets: list[Wallet]
    page: int
    page_size: int
    size_per_page: int


class DBItem(Item, SQLModel, table=True):
    __tablename = 'items'
    id:int = Field(default=None, primary_key=True)
    merchant_id: int = Field(default=None, foreign_key="merchants.id")

class DBMerchant(Merchant, SQLModel, table=True):
    __tablename__ = "merchants"
    id: Optional[int] = Field(default=None, primary_key=True)

class DBWallet(Wallet, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class DBTransaction(Transaction, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)



connect_args = {}

engine = create_engine(
    "postgresql+pg8000://postgres:123456@localhost/digimondb",
    echo=True,
    connect_args=connect_args,
)


SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/items")
async def create_item(item: CreatedItem) -> Item:
    print("create_item", item)
    data = item.dict()
    dbitem = DBItem(**data)
    with Session(engine) as session:
        session.add(dbitem)
        session.commit()
        session.refresh(dbitem)

    # return Item.parse_obj(dbitem.dict())
    return Item.from_orm(dbitem)


@app.get("/items")
async def read_items() -> ItemList:
    with Session(engine) as session:
        items = session.exec(select(DBItem)).all()

    return ItemList.from_orm(dict(items=items, page_size=0, page=0, size_per_page=0))


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> Item:
    with Session(engine) as session:
        db_item = session.get(DBItem, item_id)
        if db_item:
            return Item.from_orm(db_item)
    raise HTTPException(status_code=404, detail="Item not found")


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: UpdatedItem) -> Item:
    print("update_item", item)
    data = item.dict()
    with Session(engine) as session:
        db_item = session.get(DBItem, item_id)
        db_item.sqlmodel_update(data)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)

    return Item.from_orm(db_item)


@app.delete("/items/{item_id}")
async def delete_item(item_id: int) -> dict:
    with Session(engine) as session:
        db_item = session.get(DBItem, item_id)
        session.delete(db_item)
        session.commit()

    return dict(message="delete success")


@app.post("/merchants")
async def create_item(merchant: CreatedMerchant) -> Merchant:
    print("created_merchant", merchant)
    data = merchant.dict()
    dbitem = DBMerchant(**data)
    with Session(engine) as session:
        session.add(dbitem)
        session.commit()
        session.refresh(dbitem)

    return Merchant.from_orm(dbitem)

@app.get("/merchants")
async def read_items() -> Merchant_list:
    with Session(engine) as session:
        items = session.exec(select(DBMerchant)).all()
        
    return Merchant_list.from_orm(dict(merchants=items, page_size=0, page=0, size_per_page=0))

@app.get("/merchants/{merchant_id}")
async def read_item(merchant_id: int) -> Merchant:
    with Session(engine) as session:
        db_item = session.get(DBMerchant, merchant_id)
        if db_item:
            return Merchant.from_orm(db_item)
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/merchants/{merchant_id}")
async def update_item(merchant_id: int, item: UpdateMerchant) -> Merchant:
    print("update_item", item)
    data = item.dict()
    with Session(engine) as session:
        db_item = session.get(DBMerchant, merchant_id)
        db_item.sqlmodel_update(data)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)

    return Merchant.from_orm(db_item)

@app.delete("/merchants/{merchant_id}")
async def delete_item(merchant_id: int) -> dict:
    with Session(engine) as session:
        db_item = session.get(DBMerchant, merchant_id)
        session.delete(db_item)
        session.commit()

    return dict(message="delete success")

@app.post("/wallets")
async def create_item(wallet: CreatedWallet) -> Wallet:
    print("created_merchant", wallet)
    data = wallet.dict()
    dbitem = DBWallet(**data)
    with Session(engine) as session:
        session.add(dbitem)
        session.commit()
        session.refresh(dbitem)

    # return Item.parse_obj(dbitem.dict())
    return Wallet.from_orm(dbitem)

@app.get("/wallets")
async def read_items() -> Wallet_list:
    with Session(engine) as session:
        wallets = session.exec(select(DBWallet)).all()
        
    return Wallet_list.from_orm(dict(wallets=wallets, page_size=0, page=0, size_per_page=0))

@app.get("/wallets/{wallet_id}")
async def read_item(wallet_id: int) -> Wallet:
    with Session(engine) as session:
        db_item = session.get(DBWallet, wallet_id)
        if db_item:
            return Wallet.from_orm(db_item)
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/wallets/{wallet_id}")
async def update_item(wallet_id: int, item: UpdateWallet) -> Wallet:
    print("update_item", item)
    data = item.dict()
    with Session(engine) as session:
        db_item = session.get(DBWallet, wallet_id)
        db_item.sqlmodel_update(data)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)

    # return Item.parse_obj(dbitem.dict())
    return Wallet.from_orm(db_item)

@app.delete("/wallets/{wallet_id}")
async def delete_item(wallet_id: int) -> dict:
    with Session(engine) as session:
        db_item = session.get(DBWallet, wallet_id)
        session.delete(db_item)
        session.commit()

    return dict(message="delete success")

