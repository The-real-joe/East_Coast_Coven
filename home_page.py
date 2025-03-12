import streamlit as st
from pathlib import Path

st.markdown("# Welcome to the East Coast Coven")
st.sidebar.markdown("# Home")

# Get the current file's directory
current_dir = Path(__file__).parent

# Construct the path to the image
image_path = current_dir / "static" / "logo.png"

# Display the image
st.image(str(image_path))
