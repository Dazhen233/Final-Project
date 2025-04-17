from fastapi import APIRouter, BackgroundTasks, HTTPException, Request  # 确保引入 Request 对象
from pydantic import BaseModel
from app.core.agents.story_agent import process_with_langchain
from app.core.memory.session_manager import get_all_conversation_memory
import json
import logging

# 初始化日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置日志级别为 DEBUG
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

router = APIRouter()

class UserRequest(BaseModel):
    user_id: str
    user_input: str

@router.post("/process")
async def process_request(request: UserRequest, background_tasks: BackgroundTasks, fastapi_request: Request):
    try:
        logger.info(f"Received request: user_id={request.user_id}, user_input={request.user_input}")
        response_data = process_with_langchain(request.user_id, request.user_input, fastapi_request)
        logger.info(f"Response data: {response_data}")
        return response_data
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)  # 打印完整的异常堆栈信息
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
