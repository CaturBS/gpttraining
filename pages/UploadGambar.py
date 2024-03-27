import streamlit as st
from PIL import Image,ImageEnhance
import geminichat

st.set_page_config(page_title="Living Room", page_icon="📈")
st.write("Silahkan upload foto kamar, kamar mandi, teras atau ruangan di dalam rumah anda")

uploaded_file = st.file_uploader("Upload foto kamar, toilet, teras di rumah atau ketik teks dibawah", type=['png', 'jpg'] )

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    txt = geminichat.get_conversation(image)
    st.image(
        image,
        caption=f"You amazing image has shape",
        use_column_width=True,
    )
    st.write(txt)
