import dataclasses

import openai
import streamlit as st

from _openai_st_blocks import openai_safe_st_block, openai_st_moderation

from weird_gpt.password import ask_password


KEY_CONVERSATION = "conversation"

client = openai.OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    # api_key="My API Key",
)


@dataclasses.dataclass
class Message:
    user_prompt: str
    revised_prompt: str
    image_url: str


def start_conversation():
    if KEY_CONVERSATION not in st.session_state:
        st.session_state[KEY_CONVERSATION] = []


def on_reset_conversation():
    del st.session_state[KEY_CONVERSATION]


def converse():
    def show_conversation():
        for message in st.session_state[KEY_CONVERSATION]:
            with st.chat_message("User"):
                st.write(message.user_prompt)
            with st.chat_message("Assistant", avatar="👩‍🎨"):
                show_response(
                    image_url=message.image_url, suggested_prompt=message.revised_prompt
                )

    def show_response(*, image_url: str, suggested_prompt: str):
        st.image(image_url, use_column_width=True)
        st.write(f"[link]({image_url})")
        with st.expander("Revised prompt"):
            st.write(f"*{suggested_prompt}*")

    quality = lambda radio: radio.lower()
    style = lambda radio: radio.lower()

    st.title("🎨 Images")
    st.info("Generate images from text with OpenAI.")
    st.warning(
        "Images are relatively expensive to generate and this page can become quickly addictive, "
        "and therefore costly to the site owner."
    )

    with st.container(border=True):
        quality_radio = st.radio(
            "Quality",
            ["Standard", "HD"],
            index=1,
            horizontal=True,
        )
        model = st.radio("Model", ["dall-e-3"], index=0, horizontal=True)
        style_radio = st.radio(
            "Style",
            ["Natural", "Vivid"],
            index=0,
            horizontal=True,
            help="Vivid causes the model to lean towards generating hyper-real and dramatic images. "
            "Natural causes the model to produce more natural, less hyper-real looking images.",
        )
        size = st.radio(
            "Size",
            ["1024x1024", "1792x1024", "1024x1792"],
            index=0,
            horizontal=True,
        )

    show_conversation()

    if st.button("Reset"):
        on_reset_conversation()
        st.rerun()

    prompt = st.chat_input("Describe an image")
    if prompt:
        with st.chat_message("User"):
            st.write(prompt)
        with st.chat_message("Assistant"):
            with st.spinner("Drawing..."):
                openai_st_moderation(prompt)

                with openai_safe_st_block():
                    response = client.images.generate(
                        prompt=prompt,
                        model=model,
                        n=1,
                        quality=quality(quality_radio),
                        response_format="url",
                        style=style(style_radio),
                        size=size,
                    )
                    url = response.data[0].url
                    revised_prompt = response.data[0].revised_prompt
                    show_response(image_url=url, suggested_prompt=revised_prompt)
                    st.session_state[KEY_CONVERSATION].append(
                        Message(
                            user_prompt=prompt,
                            revised_prompt=revised_prompt,
                            image_url=url,
                        )
                    )


ask_password()

start_conversation()
converse()
