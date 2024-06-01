import random

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
st.info("Even tweaked, the chatbots may still hallucinate.")

images = [
    "s_airplane_1",
    "s_airplane_2",
    "s_alien_2",
    "s_alien_3",
    "s_alien_4",
    "s_beagle_beach_1",
    "s_cat_destroys_city_1",
    "s_cat_destroys_city_2",
    "s_cat_destroys_city_3",
    "s_dog_catching_pizza_2",
    "s_dog_catching_pizza_3",
    "s_dogs_fallout",
    "s_dogs_pubg_1",
    "s_munch"
]
random_image = random.choice(images)
st.image(f"./assets/random/{random_image}.png", use_column_width=True)
