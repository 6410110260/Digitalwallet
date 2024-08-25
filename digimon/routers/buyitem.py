from fastapi import APIRouter, HTTPException, Depends , status
from typing import Optional, Annotated
from sqlmodel import Field, SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from .. import deps
from .. import models


router = APIRouter(prefix="/buy")

@router.post("")
async def buy_item(
    transaction: models.CreatedTransaction,
    session: Annotated[AsyncSession, Depends(models.get_session)],
    current_user: models.User = Depends(deps.get_current_user),
):
    if current_user.role != "customer" :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only customer can buy items."
        )
    statement = select(models.DBItem).where(models.DBItem.id == transaction.item_id)
    result = await session.exec(statement)
    dbitem = result.one_or_none()
    

    
    statement = select(models.DBWallet).where(models.DBWallet.user_id == dbitem.user_id)
    result = await session.exec(statement)
    merchant_wallet = result.one_or_none()
    
    statement = select(models.DBWallet).where(models.DBWallet.user_id == current_user.id)
    result = await session.exec(statement)
    customer_wallet = result.one_or_none()
    
    statement = select(models.DBCustomer).where(models.DBCustomer.user_id == current_user.id)
    result = await session.exec(statement)
    dbcustomer = result.one_or_none()
    
    dbtransaction = models.DBTransection.from_orm(transaction)
    
    price = dbitem.price
    dbtransaction.price = price
    dbtransaction.merchant_id = dbitem.merchant_id
    dbtransaction.customer_id = dbcustomer.id
    
    merchant_wallet.balance += price
    customer_wallet.balance -= price
    
    merchant_wallet.sqlmodel_update(merchant_wallet)
    customer_wallet.sqlmodel_update(customer_wallet)
    session.add(dbtransaction)
    session.add(merchant_wallet)
    session.add(customer_wallet)
    await session.commit()
    await session.refresh(dbtransaction)
    
    return models.Transaction.from_orm(dbtransaction)