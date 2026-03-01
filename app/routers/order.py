from datetime import datetime

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.models import Order
from app.database import db_dep
from app.schemas.schemas import OrderRead


router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("/", response_model=list[OrderRead])
async def get_orders(session: db_dep, status: str | None = None):
    # TODO: add filter, search, pagination
    stmt = select(Order)

    if status:
        stmt = stmt.where(Order.status == status)

    res = session.execute(stmt)
    return res.scalars().all()


@router.get("/{order_id}/", response_model=OrderRead)
async def get_order(session: db_dep, order_id: int):
    stmt = select(Order).where(Order.id == order_id)
    res = session.execute(stmt)
    order = res.scalars().first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.post("/open/", response_model=OrderRead)
async def open_order(session: db_dep, table_id: int, waiter_id: int):
    order = Order(table_id=table_id, waiter_id=waiter_id, status="open")

    session.add(order)
    session.commit()
    session.refresh(order)

    return order


@router.post("/{order_id}/submit/")
async def submit_order(session: db_dep, order_id: int):
    stmt = select(Order).where(Order.id == order_id)
    res = session.execute(stmt)
    order = res.scalars().first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "open":
        raise HTTPException(status_code=400, detail="Order not open")

    order.status = "submitted"
    order.submitted_at = datetime.now()

    session.commit()
    session.refresh(order)

    return order


@router.post("/{order_id}/close/")
async def close_order(session: db_dep, order_id: int):
    stmt = select(Order).where(Order.id == order_id)
    res = session.execute(stmt)
    order = res.scalars().first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = "closed"
    order.closed_at = datetime.now()

    session.commit()
    session.refresh(order)

    return order
