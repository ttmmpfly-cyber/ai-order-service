from datetime import datetime

from pydantic import BaseModel,ConfigDict

class OrderResponse(BaseModel):
    order_id:str
    customer_name: str
    product_name: str
    amount: float
    status: str
    paid: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RefundRequest(BaseModel):
    reason:str


class RefundResponse(BaseModel):
    order_id:str
    status:str
    message:str

class ChatRequest(BaseModel):
    message:str

class ChatResponse(BaseModel):
    intent:str
    answer:str

class ChatResumeRequest(BaseModel):
    thread_id: str
    approved: bool