from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import OrderResponse
from services.order_service import get_order_by_id

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.get(
    "/{order_id}",
    response_model=OrderResponse
)

def get_order(
    order_id:str,
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

    return order