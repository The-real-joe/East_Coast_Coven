import streamlit as st
from pathlib import Path

st.markdown("# Welcome to the East Coast Coven")
st.sidebar.markdown("# Home")
st.markdown("""
<a href="https://www.facebook.com/groups/eastcoastcoven" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook" width="30" height="30">
</a>
""", unsafe_allow_html=True)


# Get the current file's directory
current_dir = Path(__file__).parent

# Construct the path to the image
image_path = current_dir / "static" / "logo.png"

# Display the image
st.image(str(image_path))