from typing import TypedDict

class ChatState(TypedDict,total=False):
    message:str
    intent:str
    order_id:str | None

    approved: bool
    refund_reason: str
    answer:str