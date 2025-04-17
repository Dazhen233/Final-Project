import whisper
import torch
import os

# 检查 PyTorch 是否使用 CPU
print("\n🔍 检查 PyTorch 版本...")
print("PyTorch 版本:", torch.__version__)
print("CUDA 是否可用:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("CUDA 版本:", torch.version.cuda)
    print("当前 GPU:", torch.cuda.get_device_name(0))
else:
    print("❌ CUDA 不可用，Whisper 只能使用 CPU 运行！")

# 确保音频文件存在
audio_file = r"H:\StoryBot\backend\test.mp3"
if not os.path.exists(audio_file):
    print(f"❌ 文件不存在: {audio_file}")
    exit()
else:
    print(f"✅ 找到音频文件: {audio_file}")

# 加载 Whisper 模型
def transcribe_audio(audio_path, model_size="small"):
    print("\n🔍 加载 Whisper 模型...")
    model = whisper.load_model(model_size)
    print(f"✅ Whisper {model_size} 模型加载成功！")

    print("\n🎙️ 转录音频...")
    result = model.transcribe(audio_path, fp16=False)
    print("✅ 转录完成！")
    print("\n📝 识别文本:")
    print(result["text"])

# 运行语音转录
transcribe_audio(audio_file, model_size="small")