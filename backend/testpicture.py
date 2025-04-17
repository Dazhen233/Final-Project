import openai
import os  # Add this import

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

response = client.images.generate(
    model="dall-e-3",
    prompt="一个动画风格的场景，包括 奥特曼, 火星, 怪兽",
    n=1,
    size="1024x1024"
)

print(response.data[0].url)  # 你应该看到一个图片链接
