from flask import Flask, send_file
import openai

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.route("/tts", methods=["GET"])
def tts():
    try:
        # 固定的文本内容
        text = "Hello! This is an AI-generated voice using OpenAI's text-to-speech technology. I hope you're having a great day!"

        # 调用 OpenAI TTS API（最新版本）
        response = openai.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )

        # 保存音频文件
        audio_file = "output.mp3"
        with open(audio_file, "wb") as f:
            f.write(response.content)  # ⚠️ 这里必须用 `.content`

        return send_file(audio_file, as_attachment=True)  # 返回 MP3 文件

    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
