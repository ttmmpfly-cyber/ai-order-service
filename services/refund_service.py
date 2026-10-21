from datetime import datetime,timezone

from sqlalchemy.orm import Session

from models import Order,Refund

def check_refund_eligibility(order:Order)->tuple[bool,str]:

    if not order.paid:
        return False, "Order has not been paid."

    if order.status == "shipped":
        return False, "Shipped orders cannot be refunded automatically."

    if order.status == "cancelled":
        return False, "Order is already cancelled."

    created_at = order.created_at

    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)

    order_age =(
        datetime.now(timezone.utc) - created_at
    ).days

    if order_age > 7:
        return False, "Order is outside the 7-day refund window."

    return True, "Order is eligible for refund."

def create_refund(
    db:Session,
    order:Order,
    reason:str
)-> Refund:

    refund =Refund(
        order_id=order.order_id,
        reason=reason,
        status="approved"
    )

    order.status= "cancelled"

    db.add(refund)
    db.commit()
    db.refresh(refund)

    return refund