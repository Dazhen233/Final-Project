import openai
import os
import uuid
from dotenv import load_dotenv
from fastapi import Request  # 引入 Request 对象

# 加载 .env 文件中的环境变量
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_tts(text, request: Request, voice="fable"):
    # 生成唯一的音频文件名
    audio_filename = f"{uuid.uuid4()}.mp3"
    audio_file_path = os.path.join("static", audio_filename)

    # 调用 OpenAI 的 TTS API
    response = openai.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text
    )

    # 保存音频到文件
    os.makedirs("static", exist_ok=True)  # 确保 static 目录存在
    with open(audio_file_path, "wb") as f:
        f.write(response.content)

    # 动态获取完整的 URL
    base_url = f"{request.base_url.scheme}://{request.base_url.netloc}"
    full_url = f"{base_url}/static/{audio_filename}"

    print(f"Generated Audio URL: {full_url}")
    return full_url
