import streamlit as st

from auth_service import login_user, signup_user
from user_storage import save_chat, get_chat_history
from agent import ask_railsaathi

st.set_page_config(
    page_title="RailSaathi AI",
    page_icon="🚆"
)

st.title("RailSaathi AI")
st.subheader("Personal Railway Travel Intelligence Assistant")


if "user" not in st.session_state:
    st.session_state.user = None


if st.session_state.user is None:

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):
            result = login_user(email, password)

            if "error" in result:
                st.error(result["error"])
            else:
                st.session_state.user = result
                st.rerun()

    with tab2:
        email = st.text_input("Email", key="signup_email")
        password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        if st.button("Create Account"):
            result = signup_user(email, password)

            if "error" in result:
                st.error(result["error"])
            else:
                st.session_state.user = result
                st.rerun()

else:

    user = st.session_state.user

    st.success("Logged in as " + user["email"])

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

    if "messages" not in st.session_state:

        history = get_chat_history(
            user["uid"],
            user["id_token"]
        )

        st.session_state.messages = []

        for chat in history:
            st.session_state.messages.append({
                "role": "user",
                "content": chat["user_message"]
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": chat["assistant_message"]
            })

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    prompt = st.chat_input("Ask RailSaathi AI...")

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):

            try:
                answer = ask_railsaathi(
                    st.session_state.messages
                )

                st.write(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                save_chat(
                    user["uid"],
                    user["id_token"],
                    prompt,
                    answer
                )

            except Exception as e:
                st.error("AI error: " + str(e))
