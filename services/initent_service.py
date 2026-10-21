import json

from services.llm_service import call_llm

SYSTEM_PROMPT="""
你是一个客服意图分类器。

你只能返回以下四种 intent:

order
refund
product
other

返回格式必须是 JSON:

{
  "intent": "order"
}

分类规则：

order:
查询订单状态、物流、是否发货等订单问题。

refund:
退款、取消订单、退钱等售后问题。

product:
商品功能、尺寸、使用方法、产品信息等问题。

other:
无法归入以上三类的问题。

不要返回解释。
不要返回 Markdown。
只返回 JSON。
"""

async def classify_intent(user_message:str)->str:
    result = await call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_message=user_message
    )

    try:
        data = json.loads(result)
        if not isinstance(data,dict):
            return "other"
        intent = data.get("intent", "other")
    except json.JSONDecodeError:
        return "other"
    
    allowed_intents ={
        "order",
        "refund",
        "product",
        "other"
    }

    if intent not in allowed_intents:
        return "other"

    return intent