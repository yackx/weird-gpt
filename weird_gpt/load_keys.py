import os


def check_openai_api_key_set():
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Set the OPENAI_API_KEY environment variable.")
