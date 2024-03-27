import streamlit as st


st.set_page_config(page_title="Living Room", page_icon="📈")
st.write("wow")

up = st.file_uploader("Upload foto kamar, toilet, teras di rumah atau ketik teks dibawah", type=['png', 'jpg'] )
cam = st.camera_input(label="Ambil foto")