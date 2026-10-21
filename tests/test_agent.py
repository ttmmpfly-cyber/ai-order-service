import pytest

from agent.graph import graph
from agent import nodes
from langgraph.types import Command

@pytest.mark.asyncio
async def test_order_node(monkeypatch):
    async def fake_classify_intent(message):
        return "order"

    async def fake_get_order(order_id):
        return{
            "found": True,
            "order_id": order_id,
            "status": "shipped"
        }
    
    monkeypatch.setattr(
        nodes,
        "classify_intent",
        fake_classify_intent
    )

    monkeypatch.setattr(
        nodes,
        "get_order_via_mcp",
        fake_get_order
    )

    state ={
        "message": "A1001 发货了吗？"
    }

    classify_result = await nodes.classify_node(
        state
    )

    assert classify_result["intent"] == "order"

    state.update(classify_result)

    order_result = await nodes.order_node(
        state
    )

    assert order_result["order_id"] == "A1001"
    assert "shipped" in order_result["answer"]

    @pytest.mark.asyncio
    async def test_product_node(monkeypatch):
        async def fake_answer_product_question(message):
            return "这款 Egg Coddler 的容量是 220ml。"
        
        monkeypatch.stattr(
            nodes,
            "answer_product_question",
            fake_answer_product_question
        )

        state ={
            "message": "这个 Egg Coddler 容量是多少？",
            "intent": "product"
        }

        result = await nodes.product_node(
            state
        )

        assert "220ml" in result["answer"]

@pytest.mark.asyncio
async def test_check_refund_node(monkeypatch):

    async def fake_check_refund(order_id):
        return{
            "eligible": True,
            "order_id": order_id,
            "reason": "Order is eligible for refund."
        }
    monkeypatch.setattr(
        nodes,
        "check_refund_via_mcp",
        fake_check_refund
    )

    state = {
        "message": "我要退款 A1002",
        "intent": "refund"
    }

    result = await nodes.check_refund_node(
        state
    )

    assert result["order_id"] == "A1002"
    assert result["refund_reason"] == "我要退款 A1002"


@pytest.mark.asyncio
async def test_refund_interrupt(monkeypatch):
    async def fake_classify_intent(message):
        return "refund"

    async def fake_check_refund(order_id):
        return {
            "eligible": True,
            "order_id": order_id,
            "reason": "Order is eligible for refund."
        }
    monkeypatch.setattr(
        nodes,
        "classify_intent",
        fake_classify_intent
    )

    monkeypatch.setattr(
        nodes,
        "check_refund_via_mcp",
        fake_check_refund
    )

    config = {
        "configurable": {
            "thread_id": "test_refund_001"
        }
    }

    result = await graph.ainvoke(
        {
            "message": "我要退款 A1002"
        },
        config=config
    )
    
    assert "__interrupt__" in result

@pytest.mark.asyncio
async def test_refund_resume(monkeypatch):
    async def fake_classify_intent(message):
        return "refund"

    async def fake_check_refund(order_id):
        return{
            "eligible": True,
            "order_id": order_id,
            "reason": "Order is eligible for refund."
        }

    async def fake_refund_order(
        order_id:str,
        reason:str
    ):
        
        return{
            "success": True,
            "order_id": order_id,
            "refund_status": "approved"
        }
    
    monkeypatch.setattr(
        nodes,
        "classify_intent",
        fake_classify_intent
    )

    monkeypatch.setattr(
        nodes,
        "check_refund_via_mcp",
        fake_check_refund
    )

    monkeypatch.setattr(
        nodes,
        "refund_order_via_mcp",
        fake_refund_order
    )

    config = {
        "configurable": {
            "thread_id": "test_refund_resume_001"
        }
    }

    first_result = await graph.ainvoke(
        {
            "message": "我要退款 A1002"
        },
        config=config
    )

    assert "__interrupt__" in first_result

    resumed_result = await graph.ainvoke(
        Command(
            resume=True
        ),
        config=config
    )

    assert resumed_result["approved"] is True
    assert "approved" in resumed_result["answer"]