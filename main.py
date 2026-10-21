from fastapi import FastAPI, Request
from routes.orders import router as orders_router
from routes.refunds import router as refunds_router
from routes.chat import router as chat_router
from fastapi.responses import JSONResponse
from logger import logger



app = FastAPI(
    title="AI Order Service",
    description="AI 智能定案客服与自动化系统",
    version="1.0.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(
    request:Request,
    exc: Exception
):  
    logger.exception(
        "Unhandled error: path=%s",
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "服务器内部发生错误，请稍后重试。"
        }
    )

app.include_router(orders_router)
app.include_router(refunds_router)
app.include_router(chat_router)


@app.get("/")
def root():
    logger.info("Root endpoint called")

    return{
        "service":"AI Order Service",
        "status":"running"
    }

@app.get("/health")
def health_check():
    logger.info("Health check called")

    return{
        "status":"ok"
    }


