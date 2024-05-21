import contextlib

import openai
import streamlit as st

from weird_gpt.moderation import moderate_aggregate


@contextlib.contextmanager
def openai_safe_st_block():
    try:
        yield
    except openai.AuthenticationError:
        st.error("Authentication error.")
        st.stop()
    except openai.OpenAIError as e:
        st.error(f"OpenAI error (${e}).")
        print(e)
        st.stop()


def openai_st_moderation(prompt: str):
    with openai_safe_st_block():
        if moderation := moderate_aggregate(prompt):
            formatted_dict = {k: "{:.2f}".format(v) for k, v in moderation.items()}
            st.warning(f"Moderation: FLAGGED {formatted_dict}")
