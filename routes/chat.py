from uuid import uuid4
from fastapi import APIRouter
from agent.graph import graph
from langgraph.types import Command
from logger import logger
from schemas import (
    ChatRequest,
    ChatResponse,
    ChatResumeRequest,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("")
async def chat(data:ChatRequest):
    logger.info(
        "Chat request received: %s",
        data.message
    )

    thread_id = str(uuid4())
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = await graph.ainvoke(
        {
            "message": data.message
        },
        config=config
    )

    if "__interrupt__" in result:
        return{
            "status": "waiting_approval",
            "thread_id": thread_id,
            "message": str(
                result["__interrupt__"][0].value
            )
        }

    return{
        "status": "completed",
        "thread_id": thread_id,
        "intent": result.get("intent", "other"),
        "answer": result.get(
            "answer",
            "暂时无法处理这个问题。"
        )
    }

@router.post("/resume")
async def resume_chat(
    data: ChatResumeRequest
):
    logger.info(
        "Resume refund workflow: thread_id=%s approved=%s",
        data.thread_id,
        data.approved
    )

    config = {
        "configurable": {
            "thread_id": data.thread_id
        }
    }

    result = await graph.ainvoke(
        Command(
            resume=data.approved
        ),
        config=config
    )

    return {
        "status": "completed",
        "thread_id": data.thread_id,
        "intent": result.get("intent", "other"),
        "answer": result.get(
            "answer",
            "流程已完成。"
        )
    }

