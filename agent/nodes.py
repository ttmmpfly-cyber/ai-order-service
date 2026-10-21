# from database import SessionLocal

# from agent.state import ChatState
# from services.initent_service import classify_intent
# from services.message_service import extract_order_id
# from services.order_service import get_order_by_id
# from services.refund_service import(
#     check_refund_eligibility,
#     create_refund
# )
# from services.rag_service import answer_product_question
from langgraph.types import interrupt
from agent.state import ChatState
from mcp_app.client import(
    get_order_via_mcp,
    refund_order_via_mcp,
    check_refund_via_mcp,
)
from services.initent_service import classify_intent
from services.message_service import extract_order_id
from services.rag_service import answer_product_question
from logger import logger

async def classify_node(state:ChatState)->ChatState:
    intent = await classify_intent(
        state["message"]
    )

    return{
        "intent":intent
    }

async def order_node(state: ChatState) -> ChatState:
    order_id = extract_order_id(
        state["message"]
    )
    if order_id is None:
        return{
            "order_id":None,
            "answer":"请提供订单号，例如 A1001"
        }

    result = await get_order_via_mcp(order_id)


    if not result.get("found"):
            return{
                "order_id": order_id,
                "answer": f"没有找到订单 {order_id}。"
            }
    return{
            "order_id": order_id,
            "answer":(
                f"订单 {order_id} 当前状态为 "
                f"{result['status']}。"
            )
        }

async def check_refund_node(
    state: ChatState
) -> ChatState:
    order_id = extract_order_id(
        state["message"]
    )

    if order_id is None:
        return{
            "order_id": None,
            "answer": "请提供需要退款的订单号，例如 A1002。"
        }
    result = await check_refund_via_mcp(
        order_id
    )

    if not result.get("eligible"):
        reason = result.get(
            "reason",
            result.get(
                "error",
                "退款资格检查失败"
            )
        )

        return{
            "order_id": order_id,
            "eligible": False,
            "answer": (
                f"订单 {order_id} 不符合退款条件："
                f"{reason}"
            )
        }
    return{
        "order_id": order_id,
        "eligible": True,
        "refund_reason": state["message"]
    }

async def approval_node(
    state: ChatState
) -> ChatState:
   order_id = state["order_id"]

   approved = interrupt(
        f"订单 {order_id} 符合退款条件，是否批准退款？"
   )

   return{
       "approved": bool(approved)
   }

async def execute_refund_node(
    state: ChatState
) -> ChatState:
    order_id = state["order_id"]
    
    result = await refund_order_via_mcp(
        order_id= order_id,
            reason=state.get(
            "refund_reason",
            state["message"]
        )
    )

    if not result.get("success"):
        reason = result.get(
            "reason",
            result.get(
                "error",
                "退款失败"
            )
        )

        return{
            "answer": (
                f"订单 {order_id} 退款失败："
                f"{reason}"
            )
        }
    
    logger.info(
        "Refund approved: order_id=%s",
        order_id
    )

    return{
        "answer": (
            f"订单 {order_id} 退款申请已通过，"
            f"退款状态为 "
            f"{result['refund_status']}。"
        )
    }

def reject_refund_node(
    state: ChatState
) -> ChatState:
   
    return{
        "answer": (
            f"订单 {state['order_id']} "
            f"的退款申请未获人工批准。"
        )
    }


# async def refund_node(state: ChatState) -> ChatState:
#     order_id = extract_order_id(
#         state["message"]
#     )
#     if order_id is None:
#         return{
#             "order_id": None,
#             "answer": "请提供需要退款的订单号，例如 A1002。"
#         }
    
#     result = await refund_order_via_mcp(
#         order_id=order_id,
#         reason=state["message"]
#     )

#     if not result.get("success"):
#         reason = result.get(
#             "reason",
#             result.get(
#                 "error",
#                 "退款失败"
#             )
#         )

#         return {
#             "order_id": order_id,
#             "answer": (
#                 f"订单 {order_id} 无法退款："
#                 f"{reason}"
#             )
#         }

#     return {
#         "order_id": order_id,
#         "answer": (
#             f"订单 {order_id} 退款申请已通过，"
#             f"退款状态为 "
#             f"{result['refund_status']}。"
#         )
#     }

async def product_node(state:ChatState)->ChatState:
    answer = await answer_product_question(
        state["message"]
    )
    return{
        "answer":answer
    }

def other_node(state:ChatState)->ChatState:
    return{
        "answer":"暂时无法处理这个问题"
    }