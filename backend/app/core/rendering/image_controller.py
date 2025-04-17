import os
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import base64
from fastapi import Request

# 加载 .env 环境变量
load_dotenv()
stability_api_key = os.getenv("STABILITY_API_KEY")

# REST API 的基础 URL
REST_API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image"

# 请求头部信息
HEADERS = {
    "Authorization": f"Bearer {stability_api_key}"
}

def generate_image(story_text, character_image_path, request: Request):
    prompt = f"Generate an image based on the following story: {story_text}"

    try:
        with open("character_images/snow_white.png", "rb") as image_file:
            init_image = Image.open(image_file).convert("RGB")
            init_image = init_image.resize((1024, 1024))  # resize to valid SDXL size
            buffer = BytesIO()
            init_image.save(buffer, format="PNG")
            init_image_bytes = buffer.getvalue()
    except Exception as e:
        print("❌ Failed to load or process character image:", e)
        return None

    # 构造 POST 请求的数据
    files = {
        "init_image": ("init_image.png", init_image_bytes, "image/png"),
    }

    payload = {
        "text_prompts[0][text]": prompt,
        "cfg_scale": 7,
        "image_strength": 0.35,
        "steps": 50,
        "samples": 1,
    }

    try:
        response = requests.post(REST_API_URL, headers=HEADERS, files=files, data=payload)
    except Exception as e:
        print("❌ Request failed:", e)
        return None

    if response.status_code != 200:
        print("❌ Error response from API:", response.status_code, response.text)
        return None

    try:
        result = response.json()
        artifacts = result.get("artifacts", [])
        for idx, artifact in enumerate(artifacts):
            if artifact.get("finishReason") == "CONTENT_FILTERED":
                print("🚫 Content was filtered by safety system.")
                return None
            if "base64" in artifact:
                image_data = base64.b64decode(artifact["base64"])
                os.makedirs("static", exist_ok=True)
                image_path = f"static/generated_{idx}.png"
                with open(image_path, "wb") as f:
                    f.write(image_data)
                print(f"✅ Image saved to: {image_path}")

                # 动态获取完整的 URL
                base_url = f"{request.base_url.scheme}://{request.base_url.netloc}"
                full_url = f"{base_url}/{image_path}"
                return full_url
    except Exception as e:
        print("❌ Failed to parse image from response:", e)

    print("⚠️ No image was returned.")
    return None


if __name__ == "__main__":
    test_story = "A beautiful girl with black hair and pale skin lives in a forest with seven dwarfs."
    test_image_path = "C:/Users/Steven/Downloads/StoryBot-Final-Project/backend/character_images/snow_white.png"
    # The `request` parameter is required for the updated `generate_image` function.
    print("❌ Failed to generate image due to missing `request` parameter in standalone execution.")
