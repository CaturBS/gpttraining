import logging
import os
import time
import streamlit as st
import geminitext
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
import streamlit.components.v1 as components


# import os

def get_remote_ip():
    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None
        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None

        return session_info.request.remote_ip
    except Exception as e:
        return None


class ContextFilter(logging.Filter):
    def filter(self, record):
        record.user_ip = get_remote_ip()
        return super().filter(record)
def init_logging():
    logger = logging.getLogger("streamlitlogger")
    if logger.handlers:
        return
    logger.propagate = False
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s [user_ip=%(user_ip)s] - %(message)s")
    handler = logging.FileHandler(os.path.join(os.getcwd(),"logger.log"))
    handler.setLevel(logging.INFO)
    handler.addFilter(ContextFilter())
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def _get_stream(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)


if __name__ == '__main__':
    st.set_page_config(
        page_title="RumahHarmoni",
        page_icon="👋",
        layout="wide",
        menu_items={
            'Get Help': 'http://www.rumahharmoni.my.id/help',
            'Report a bug': "http://www.rumahharmoni.my.id//bug",
            'About': "# This is a header. This is an *extremely* cool app!"
        }
    )
    init_logging()

    logger = logging.getLogger("streamlitlogger")
    st.title("Rumah Harmoni")
    logger.info("remoteip:\t"+get_remote_ip())
    st.code("author: ctrbudisantoso@gmail.com\npage: http://www.rumahharmoni.my.id/")
    with st.chat_message("assistant"):
        st.markdown(
            '<img src="./app/static/cozy.jpg" height="150" style="border: 1px solid orange">',
            unsafe_allow_html=True,
        )
        # st.write("Upload Gambar [link](%s)" % url)
        # st.markdown("Upload Gambar [link](%s)" % url)
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat" not in st.session_state:
        st.session_state.chat = geminitext.get_chat()
        response_body = st.session_state.chat.send_message("Rumah Harmoni tolong sapa user dan beri deskripsi tentang anda. Serta persilahkan user untuk menggunakan fasilitas chat dari anda.")
        resp = response_body.parts[0].text
        st.write_stream(_get_stream(resp))
        st.session_state.messages.append({"role": "assistant", "content": resp, "type":"text"})
    else:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if "type" in message:
                    if message["type"] == "image":
                        st.image(
                            message["content"],
                            caption=f"Foto dari user",
                            use_column_width=True,
                        )
                    else:
                        # st.write_stream(_get_stream(message["content"]))
                        st.markdown(message["content"])
                else:
                    # st.write_stream(_get_stream(message["content"]))
                    st.markdown(message["content"])


    prompt = st.chat_input("Chat disini")
    if prompt:
        with st.chat_message("user"):
            st.write(f"{prompt}")
        response_body = st.session_state.chat.send_message(prompt)
        response = str(response_body.parts[0].text)
        with st.chat_message("assistant"):
            # st.markdown(response)
            st.write_stream(_get_stream(response))
        st.session_state.messages.append({"role": "user", "content": prompt, type:"text"})
        st.session_state.messages.append({"role": "assistant", "content": response, type:"text"})



    with st.chat_message("assistant"):
        st.write("Anda bisa upload foto kamar, toilet atau teras di rumah untuk mendapatkan saran-saran dari saya.")
        st.page_link('pages/UploadGambar.py', label="Klik disini untuk meng-upload gambar",icon="👆")