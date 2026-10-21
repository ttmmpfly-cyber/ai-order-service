from fastapi import APIRouter,Depends,HTTPException

from sqlalchemy.orm import Session

from database import get_db
from schemas import RefundRequest, RefundResponse
from services.order_service import get_order_by_id
from services.refund_service import (
    check_refund_eligibility,
    create_refund
)

router = APIRouter(
    prefix="/refunds",
    tags=["Refunds"]
)

@router.post(
    "/{order_id}",
    response_model=RefundResponse
)
def refund_order(
    order_id:str,
    data:RefundRequest,
    db:Session = Depends(get_db)
):

    order = get_order_by_id(
        db=db,
        order_id=order_id
    )
    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    eligible, reason = check_refund_eligibility(order)
    
    if not eligible:
        raise HTTPException(
            status_code=400,
            detail=reason
        )
    
    refund = create_refund(
        db=db,
        order=order,
        reason=data.reason
    )
    return {
        "order_id": refund.order_id,
        "status": refund.status,
        "message": "Refund approved successfully."
    }