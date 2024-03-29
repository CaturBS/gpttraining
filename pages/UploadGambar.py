import streamlit as st
from PIL import Image,ImageEnhance
import geminichat

st.set_page_config(page_title="Living Room", page_icon="📈")
st.write("Silahkan upload foto kamar, kamar mandi, teras atau ruangan di dalam rumah anda")

uploaded_file = st.file_uploader("Upload foto kamar, toilet, teras di rumah atau ketik teks dibawah", type=['png', 'jpg'] )

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    response_body = geminichat.get_conversation(image)
    img = st.image(
        image,
        caption=f"You amazing image has shape",
        use_column_width=True,
    )
    try:
        txt = str(response_body.parts[0].text)
        st.write(txt)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        st.session_state.messages.append({"role": "user", "content": image, "type": "image"})
        st.session_state.messages.append({"role": "assistant", "content": txt, "type": "text"})
    except:
        st.markdown("Maaf terjadi gangguan dalam proses analisa image. Coba gunakan browser firefox di pc.")
        st.code(response_body)

    st.page_link('chat.py', label="Klik disini untuk kembali ke chat", icon="👆")