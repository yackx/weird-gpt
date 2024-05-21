import dataclasses
import os
from typing import Optional

import streamlit as st

from weird_gpt.assistants import Assistant, ChatCompletionBot, assistants
from weird_gpt.load_keys import check_openai_api_key_set
from weird_gpt.password import ask_password
from _openai_st_blocks import openai_safe_st_block, openai_st_moderation

DEFAULT_MODEL = "gpt-4o"
DEFAULT_NB_TOKENS = 4000

# Environment variables
ENV_MODEL = "WEIRD_GPT_MODEL"
ENV_NB_TOKENS = "WEIRD_GPT_NB_TOKENS"

# st.session keys
KEY_ASSISTANT = "assistant"
KEY_CHATBOT = "chatbot"
KEY_OPENAI_KEY = "openai_key"
KEY_PARAMS_INFO = "params_info"


@dataclasses.dataclass
class Settings:
    model: str = DEFAULT_MODEL
    nb_tokens: int = DEFAULT_NB_TOKENS


def load_settings() -> Settings:
    return Settings(
        model=os.getenv(ENV_MODEL, DEFAULT_MODEL),
        nb_tokens=int(os.getenv(ENV_NB_TOKENS, DEFAULT_NB_TOKENS)),
    )


def find_assistant_by_name(name: str) -> Optional[Assistant]:
    try:
        return next(a for a in assistants if a.name == name)
    except StopIteration:
        return None


def on_delete_last_message():
    st.session_state[KEY_CHATBOT].drop_last()


def chat():
    # Assistant is already selected. Chat.
    chatbot: ChatCompletionBot = st.session_state[KEY_CHATBOT]
    assistant: Assistant = st.session_state[KEY_ASSISTANT]

    st.title(assistant.emoji + " " + assistant.name)
    st.info(st.session_state[KEY_PARAMS_INFO])

    col1, col2 = st.columns([0.3, 0.8])
    with col1:
        if st.button("End conversation"):
            del st.session_state[KEY_ASSISTANT]
            st.rerun()
    with col2:
        if st.button("Reset"):
            chatbot.reset()
            st.rerun()

    for message in chatbot.get_messages():
        with st.chat_message(message["role"]):
            st.write(message["content"])
    prompt = st.chat_input("Say something")

    if prompt:
        # Handle user input.
        with st.chat_message("User"):
            st.write(prompt)
        with st.chat_message("Assistant"):
            openai_st_moderation(prompt)
            with st.spinner("Thinking..."):
                with openai_safe_st_block():
                    response, dropped_count = chatbot.chat_completion(prompt)
                    st.write(response)
                    if dropped_count > 0:
                        st.write(f"Dropped {dropped_count} messages")
                    st.button("Delete", on_click=on_delete_last_message)


def select_assistant():
    def get_model_from_radio():
        match model_radio:
            case "GPT 3.5 turbo":
                return "gpt-3.5-turbo"
            case "GPT 4":
                return "gpt-4"
            case "GPT 4o":
                return "gpt-4o"

    st.title("💬 Weird Assistants")
    names = ["-"]  # default selection
    names.extend([a.name for a in assistants])
    name = st.selectbox("Choose your assistant", names)

    if assistant := find_assistant_by_name(name):
        st.info(assistant.description)
        model_radio = st.radio(
            "ChatGPT model",
            ["GPT 3.5 turbo", "GPT 4", "GPT 4o"],
            captions=["Cheapest", "Still good", "Shiny new"],
            index=2,
            horizontal=True,
        )
        nb_tokens = st.number_input(
            "Max tokens",
            min_value=500,
            max_value=16000,
            value=4000,
            step=500,
        )
        if assistant.code not in st.session_state:
            if st.button("Start conversation"):
                st.session_state[KEY_ASSISTANT] = assistant
                model = get_model_from_radio()
                st.session_state[KEY_PARAMS_INFO] = (
                    f"model={model} "
                    f"tokens={nb_tokens} "
                    f"t={assistant.parameters['temperature']} "
                    f"top_p={assistant.parameters['top_p']} "
                    f"fp={assistant.parameters['frequency_penalty']} "
                    f"pp={assistant.parameters['presence_penalty']} "
                )
                chatbot = ChatCompletionBot(
                    model=model,
                    model_parameters=assistant.parameters,
                    max_tokens=nb_tokens,
                    system_prompt=assistant.system_prompt,
                )
                st.session_state[KEY_CHATBOT] = chatbot
                st.rerun()
    else:
        # Default selection.
        st.info("Please choose an assistant to continue.")


if KEY_OPENAI_KEY not in st.session_state:
    try:
        check_openai_api_key_set()
        st.session_state[KEY_OPENAI_KEY] = True
    except ValueError:
        st.error("OpenAI API key missing.")
        st.stop()

ask_password()

if KEY_ASSISTANT in st.session_state:
    chat()
else:
    select_assistant()
