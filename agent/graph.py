from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import InMemorySaver
from agent.state import ChatState
from agent.nodes import(
    classify_node,
    order_node,
    check_refund_node,
    approval_node,
    execute_refund_node,
    reject_refund_node,
    product_node,
    other_node,
)

def route_intent(state:ChatState)->str:
    intent = state.get("intent","other")

    if intent =="order":
        return "order"

    if intent == "refund":
        return "check_refund"

    if intent == "product":
        return "product"

    return "other"
def route_after_refund_check(state: ChatState) -> str:
    if state.get("order_id") is None:
        return "end"

    if "answer" in state:
        return "end"

    return "approval"

def route_approval(state: ChatState) -> str:
    if state.get("approved") is True:
        return "execute_refund"

    return "reject_refund"
builder = StateGraph(ChatState)

builder.add_node(
    "classify",
    classify_node
)

builder.add_node(
    "order",
    order_node
)

builder.add_node(
    "check_refund",
    check_refund_node
)

builder.add_node(
    "approval",
    approval_node
)

builder.add_node(
    "execute_refund",
    execute_refund_node
)

builder.add_node(
    "reject_refund",
    reject_refund_node
)

builder.add_node(
    "product",
    product_node
)

builder.add_node(
    "other",
    other_node
)


builder.add_edge(
    START,
    "classify"
)

builder.add_conditional_edges(
    "classify",
    route_intent,
    {
        "order": "order",
        "check_refund": "check_refund",
        "product": "product",
        "other": "other",
    }
)

builder.add_conditional_edges(
    "check_refund",
    route_after_refund_check,
    {
        "approval": "approval",
        "end": END,
    }
)


builder.add_conditional_edges(
    "approval",
    route_approval,
    {
        "execute_refund": "execute_refund",
        "reject_refund": "reject_refund",
    }
)
builder.add_edge(
    "order",
    END
)

builder.add_edge(
    "execute_refund",
    END
)

builder.add_edge(
    "reject_refund",
    END
)

builder.add_edge(
    "product",
    END
)

builder.add_edge(
    "other",
    END
)


checkpointer = InMemorySaver()


graph = builder.compile(
    checkpointer=checkpointer
)