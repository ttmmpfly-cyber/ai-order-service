from mcp.server import MCPServer
from database import SessionLocal
from services.order_service import get_order_by_id
from services.refund_service import(
    check_refund_eligibility,
    create_refund,
)

mcp = MCPServer("OrderService")


@mcp.tool()
def get_order(order_id:str)->dict:
    db = SessionLocal()
    try:
        order = get_order_by_id(
            db=db,
            order_id=order_id
        )
        if order is None:
            return{
                "found":False,
                "order_id":order_id
            }
        return{
            "found":True,
            "order_id":order.order_id,
            "customer_name": order.customer_name,
            "product_name": order.product_name,
            "amount": order.amount,
            "status": order.status,
            "paid": order.paid
        }
    finally:
        db.close()

@mcp.tool()
def check_refund(order_id: str) -> dict:
    db = SessionLocal()

    try:
        order =get_order_by_id(
           db=db,
           order_id=order_id
        )

        if order is None:
            return{
                "eligible":False,
                "order_id":order_id,
                "reason":"Order not found"
            }
        eligible, reason = check_refund_eligibility(
            order
        )

        return{
            "eligible": eligible,
            "order_id": order_id,
            "reason": reason
        }
    finally:
        db.close()

@mcp.tool()
def refund_order(
    order_id:str,
    reason:str
)->dict:
    db =SessionLocal()

    try:
        order =get_order_by_id(
            db=db,
            order_id=order_id
        )

        if order is None:
            return{
                "success": False,
                "order_id": order_id,
                "reason": "Order not found"
            }
        eligible,eligibility_reason = (
            check_refund_eligibility(order)
        )
        if not eligible:
            return{
                "success":False,
                "order_id":order_id,
                "reason":eligibility_reason
            }
        refund = create_refund(
            db=db,
            order=order,
            reason=reason
        )
        return{
            "success": True,
            "order_id": refund.order_id,
            "refund_status": refund.status
        }
    finally:
        db.close()

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8001
    )