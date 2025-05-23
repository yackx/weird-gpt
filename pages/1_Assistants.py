from typing import Optional

import streamlit as st

from _openai_st_blocks import openai_safe_st_block, openai_st_moderation
from weird_gpt.assistants import Assistant, ChatCompletionBot, assistants
from weird_gpt.load_keys import check_openai_api_key_set
from weird_gpt.password import ask_password

DEFAULT_NB_TOKENS = 4000

# st.session keys
KEY_ASSISTANT = "assistant"
KEY_CHATBOT = "chatbot"
KEY_OPENAI_KEY = "openai_key"
KEY_MODEL_PARAMS_INFO = "model_params_info"
KEY_MODEL_DESCRIPTION = "model_description"


def find_assistant_by_name_selector(name_selector: str) -> Optional[Assistant]:
    try:
        return next(a for a in assistants if a.name_selector() == name_selector)
    except StopIteration:
        return None


def on_delete_last_message():
    st.session_state[KEY_CHATBOT].drop_last()


def chat():
    # Assistant is already selected. Chat.
    chatbot: ChatCompletionBot = st.session_state[KEY_CHATBOT]
    assistant: Assistant = st.session_state[KEY_ASSISTANT]

    st.title(assistant.emoji + " " + assistant.name)
    st.info(st.session_state[KEY_MODEL_DESCRIPTION])

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

    if len(chatbot.get_messages()) > 1:
        st.button("Delete", on_click=on_delete_last_message)


def select_assistant():
    st.title("💬 Weird Assistants")
    names = ["-"]  # default selection
    names.extend([a.name_selector() for a in assistants])
    name = st.selectbox("Choose your assistant", names)

    if assistant := find_assistant_by_name_selector(name):
        st.info(assistant.description)
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
                model = assistant.model or assistants.DEFAULT_MODEL
                st.session_state[KEY_MODEL_PARAMS_INFO] = (
                    f"model={model} "
                    f"tokens={nb_tokens} "
                    f"t={assistant.parameters['temperature']} "
                    f"top_p={assistant.parameters['top_p']} "
                    f"fp={assistant.parameters['frequency_penalty']} "
                    f"pp={assistant.parameters['presence_penalty']} "
                )
                st.session_state[KEY_MODEL_DESCRIPTION] = f"{assistant.description}"
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
