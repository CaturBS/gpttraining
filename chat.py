import time
import streamlit as st
import geminitext


# import os


def _get_stream(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.1)


if __name__ == '__main__':
    st.set_page_config(
        page_title="RumahHarmoni",
        page_icon="👋",
        layout="wide",
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )

    with st.chat_message("assistant"):
        st.markdown(
            '<img src="./app/static/cozy.jpg" height="150" style="border: 1px solid orange">',
            unsafe_allow_html=True,
        )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat" not in st.session_state:
        st.session_state.chat = geminitext.get_chat()
        response_body = st.session_state.chat.send_message("Rumah Harmoni tolong beri sapa user dan deskripsi tentang anda. Serta persilahkan user untuk menggunakan fasilitas chat dari anda.")
        resp = response_body.parts[0].text
        st.session_state.messages.append({"role": "assistant", "content": resp})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Say something")
    if prompt:
        with st.chat_message("user"):
            st.write(f"{prompt}")
        response_body = st.session_state.chat.send_message(prompt)
        response = response_body.parts[0].text
        with st.chat_message("assistant"):
            st.markdown(response)
            # st.write_stream(_get_stream(response))
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": response})