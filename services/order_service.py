from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Order

def get_order_by_id(
    db:Session,
    order_id:str,
)->Order | None:

    stmt = select(Order).where(
        Order.order_id == order_id
    )

    order = db.scalar(stmt)

    return order