import os
import streamlit as st


KEY_USER_VALID_PASSWORD = "user_valid_password"
ENV_PASSWORD = "WEIRD_GPT_PASSWORD"


# Not using st.secrets as it is not straightforward
# outside their promoted cloud environment
def load_app_password() -> str:
    return os.environ.get(ENV_PASSWORD)


def ask_password():
    if KEY_USER_VALID_PASSWORD in st.session_state:
        # Check user already authenticated
        return
    app_password = load_app_password()
    match app_password:
        case None:
            st.error(
                "Password protection misconfigured. This site will not accept login at the moment."
            )
            st.stop()
        case "":
            st.session_state[KEY_USER_VALID_PASSWORD] = True
            return
        case _:
            # Ask user password
            password = st.text_input("Password", type="password")
            if password:
                if password == app_password:
                    st.session_state[KEY_USER_VALID_PASSWORD] = True
                    st.success("Correct password")
                    st.rerun()
                else:
                    st.error("Incorrect password")
                    st.stop()
            else:
                st.stop()

    # One last for safety
    # noinspection PyUnreachableCode
    st.stop()
