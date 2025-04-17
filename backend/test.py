from app.core.agents.story_agent import *
if __name__ == "__main__":
    # 测试 process_user_input 函数
    user_id = "test_user"
    user_input = "我想和Thomas一起去冒险！"
    intent, character, next_action, reply = process_user_input(user_id, user_input)
    print(f"Intent: {intent}, Character: {character}, Next Action: {next_action}, reply: {reply}")

    # 测试 generate_story 函数
    story_data = generate_story(user_id, "thomas", "", "")
    print(f"Generated Story: {story_data['story_text']}")

    # 测试 generate_image_task 函数
    image_url = generate_image_task(story_data["story_text"], "thomas")
    print(f"Generated Image URL: {image_url}")

    # 测试 generate_tts_task 函数
    audio_url = generate_tts_task(story_data["story_text"])
    print(f"Generated Audio URL: {audio_url}")

    # 测试 process_with_langchain 函数
    result = process_with_langchain(user_id, user_input)
    print(f"Process with LangChain Result: {result}")
