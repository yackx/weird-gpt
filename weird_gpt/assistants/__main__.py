from weird_gpt.assistants import ChatCompletionBot, generic_assistant
from weird_gpt.load_keys import check_openai_api_key_set

MODEL = "gpt-4o"
NB_TOKENS = 4000


if __name__ == "__main__":
    check_openai_api_key_set()
    chat = ChatCompletionBot(
        model=MODEL,
        model_parameters=generic_assistant["parameters"],
        max_tokens=NB_TOKENS,
        system_prompt=generic_assistant["system_prompt"],
    )
    while user_input := input("? - "):
        answer, _ = chat.chat_completion(user_input)
        print(answer)
