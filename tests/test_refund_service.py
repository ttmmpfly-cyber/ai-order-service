from services.order_service import get_order_by_id
from services.refund_service import check_refund_eligibility

def test_shipped_order_cannot_refund(db):

        order = get_order_by_id(
            db=db,
            order_id="A1001"
        )

        eligible,reason = check_refund_eligibility(order)

        assert eligible is False
        assert "shipped" in reason.lower()



def test_processing_paid_order_dan_refund(db):

        order =get_order_by_id(
            db=db,
            order_id="A1002"
        )

        eligible, reason = check_refund_eligibility(order)

        assert eligible is True



def test_canclled_order_cannot_refund(db):


        order = get_order_by_id(
            db=db,
            order_id="A1003"
        )

        eligible, reason = check_refund_eligibility(order)

        assert eligible is False

