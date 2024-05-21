import streamlit as st

from weird_gpt.load_keys import check_openai_api_key_set

try:
    check_openai_api_key_set()
except ValueError:
    st.error("OpenAI API key missing.")
    with st.sidebar:
        openai_api_key = st.text_input(
            "OpenAI API Key", key="chatbot_api_key", type="password"
        )
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

st.title("💬 Weird GPT")
st.subheader("Tweaked OpenAI ChatGPT assistants")
st.markdown("Even tweaked, the chatbots may still hallucinate.")
