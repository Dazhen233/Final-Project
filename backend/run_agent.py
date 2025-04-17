# run_agent.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware  # 导入 CORS 中间件
from app.api.routes import story
from app.core.memory.session_manager import create_tables
import logging
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Creating tables...")
    create_tables()
    logger.info("Tables created successfully.")
    yield
    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（可以根据需要限制特定来源）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

app.include_router(story.router, prefix="/story", tags=["story"])

# 提供静态文件服务
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Hello, Welcome to StoryBot!"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the server...")
    uvicorn.run("run_agent:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
    logger.info("Server started successfully.")