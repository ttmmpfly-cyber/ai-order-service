# from database import SessionLocal
from services.order_service import get_order_by_id

def test_get_existing_order(db):

        order = get_order_by_id(
            db=db,
            order_id="A1001"
        )

        assert order is not None
        assert order.order_id =="A1001"
        assert order.status == "shipped"



def test_get_nonexistent_order(db):

        order =get_order_by_id(
            db=db,
            order_id="A9999"
        )

        assert order is None
