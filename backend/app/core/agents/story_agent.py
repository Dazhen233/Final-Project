import os
import json
from jinja2 import Template
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.memory import ConversationBufferMemory
from app.core.memory.session_manager import (
    get_story_state, add_story_state, 
    get_conversation_memory, add_conversation_memory, 
    get_user_character, update_user_character
)
from app.core.rendering.image_controller import generate_image
from dotenv import load_dotenv
import re
from fastapi import Request  # 确保引入 Request 对象

# 加载 .env 文件中的环境变量
load_dotenv()

# 读取 OpenAI API 密钥
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("请设置环境变量 OPENAI_API_KEY，否则无法调用 OpenAI API！")

# 初始化 OpenAI LLM
llm = OpenAI(api_key=api_key)

# 读取对话模板
with open("app/utils/prompts/dialog.jinja2", "r", encoding="utf-8") as file:
    PROMPT_TEMPLATE = Template(file.read())

# 读取故事生成模板
with open("app/utils/prompts/generate_story.jinja2", "r", encoding="utf-8") as file:
    STORY_PROMPT_TEMPLATE = Template(file.read())

# 初始化 LangChain 内存
conversation_memory = ConversationBufferMemory(memory_key="conversation_history")


def process_user_input(user_id, user_input):
    """处理用户输入，并从 LLM 生成响应"""
    conversation_history = get_conversation_memory(user_id)

    # 渲染 Jinja2 提示词模板
    prompt = PROMPT_TEMPLATE.render(
        user_input=user_input,
        conversation_history=conversation_history,
    )
    response = llm.invoke(prompt)
    print("control agent Info:===>", llm)

    if response is None:
        print("\n⚠️ Warning: LLM returned None!\n")
    elif isinstance(response, str) and response.strip() == "":
        print("\n⚠️ Warning: LLM returned an empty string!\n")
    else:
        print("response:======>", response)

    # 解析 JSON 响应
    try:
        response_json = json.loads(response)
        print("response JSON 转换成功！")
    except json.JSONDecodeError as e:
        print("JSON 转换失败！")
        print(f"错误信息：{e}")
        response_json = json.loads(json.dumps({
            'intent': 'user_dialogue', 
            'reply': 'I am sorry, I am not able to understand you. do you like Cinderella?'
        }))

    # 提供默认值
    intent = response_json.get("intent", "user_dialogue")
    character = response_json.get("character", "default_character")
    next_action = response_json.get("next_action", None)
    reply = response_json.get("reply", "I am sorry, I am not able to understand you.")

    # 记录对话历史
    add_conversation_memory(user_id, user_input, json.dumps(response_json))

    return intent, character, next_action, reply


def parse_response(response):
    # 匹配 story、question 和 word1, word2, word3 的值
    story_match = re.search(r'(?:- story\s+|story\s*=\s*|story:\s*)(.+?)(?:(?=\n[a-zA-Z]+:)|$)', response, re.DOTALL)
    question_match = re.search(r'(?:- question\s+|question\s*=\s*|question:\s*)(.+?)(?:(?=\n[a-zA-Z]+:)|$)', response, re.DOTALL)
    word_matches = re.findall(r'(?:- word\d\s+|word\d\s*=\s*|word\d:\s*)(\w+)', response)

    # 构造结果字典
    story_data = {
        "story": story_match.group(1).strip() if story_match else "",
        "question": question_match.group(1).strip() if question_match else "",
        "word1": word_matches[0] if len(word_matches) > 0 else "",
        "word2": word_matches[1] if len(word_matches) > 1 else "",
        "word3": word_matches[2] if len(word_matches) > 2 else "",
    }

    return story_data


def generate_story(user_id, user_input, character_name, difficulty_level=3):
    """生成故事"""
    conversation_history = get_conversation_memory(user_id)
    current_state = get_story_state(user_id) or "Once upon a time..."

    # 渲染 Jinja2 提示词模板
    prompt = STORY_PROMPT_TEMPLATE.render(
        difficulty_level=difficulty_level,
        character_name=character_name,
        current_state=current_state,
        last_question_answer=user_input
    )

    response = llm.invoke(prompt, max_tokens=1000)
    try:
        # 尝试将字符串转换为 JSON（Python 字典）
        response_json = json.loads(response)
        story_data = {
            "story": response_json.get("story", ""),
            "question": response_json.get("question", ""),
            "word1": response_json.get("word1", ""),
            "word2": response_json.get("word2", ""),
            "word3": response_json.get("word3", ""),
        }
        print("story JSON 转换成功！")
    except json.JSONDecodeError as e:
        # 如果 JSON 解析失败，捕获异常并打印错误信息
        print("story JSON 转换失败！")
        print(f"错误信息：{e}")

        # 使用正则提取字段
        story_data = parse_response(response)

    # 保存故事状态
    add_story_state(user_id, f"child reply: {user_input} {response}")
    print("raw story response====>", response)
    print("story text:=====>", story_data)
    return story_data


def generate_image_task(story_text, character_name, request: Request):
    """生成故事对应的图片"""
    print("DBG===> starting generate image")
    # 如果 character_name 为 None，使用默认值
    character_name = character_name or "default_character"
    character_image_path = f"character_images/{character_name.lower()}.png"
    return generate_image(story_text, character_image_path, request)


def generate_tts_task(response_text, request: Request):
    """生成故事的语音"""
    from app.core.rendering.tts_controller import generate_tts
    print("DBG===> starting generate tts")
    return generate_tts(response_text, request=request, voice="fable")


def process_with_langchain(user_id, user_input, request: Request):
    """主逻辑：处理用户输入，执行对应任务"""
    intent, character, next_action, reply = process_user_input(user_id, user_input)
    print(f"Intent: ====> {intent}, Character: {character}, Next Action: {next_action}, reply :{reply}")

    # 如果 character 为 None，设置默认值
    character = character or "default_character"

    if True:  # intent == "choose_character":
        # 更新用户选择的角色
        update_user_character(user_input, character)
        
        # 生成故事
        story_data = generate_story(user_id, user_input, character)
        print(f"Story Text: {story_data['story']}")

        # 生成图片 & 语音
        story_data['image_url'] = generate_image_task(story_data["story"], character, request)
        story_data['audio_url'] = generate_tts_task(story_data["story"], request)
        print("DBG==> finish generate image and tts")
        return story_data

    elif intent == "continue_story":
        character_name = get_user_character(user_id) or "Cinderella"
        update_user_character(user_id, character_name)

        # 生成故事
        story_data = generate_story(user_id, user_input, character_name)
        print(f"Story Text: {story_data['story_text']}")

        # 生成图片 & 语音
        story_data['image_url'] = generate_image_task(story_data["story_text"], character_name, request)
        story_data['audio_url'] = generate_tts_task(story_data["story_text"], request)

        return story_data

    elif intent == "change_character":
        update_user_character(user_id, character)
        print(f"Change Character: {character}")
        story_data = generate_story(user_id, user_input, character)
        print(f"Story Text: {story_data['story_text']}")

        # 生成图片 & 语音
        story_data['image_url'] = generate_image_task(story_data["story_text"], character, request)
        story_data['audio_url'] = generate_tts_task(story_data["story_text"], request)

        return story_data

    elif intent == 'ask_question':
        story_data = {}
        story_data['story_text'] = reply
        story_data['audio_url'] = generate_tts_task(story_data["story_text"], request)
        return story_data

    else:  # "user_dialogue"
        story_data = {}
        story_data['story_text'] = reply
        story_data['audio_url'] = generate_tts_task(story_data["story_text"], request)
        return story_data

