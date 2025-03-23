import streamlit as st
from pathlib import Path

# Set the page title and icon
st.markdown("# Merch")
st.sidebar.markdown("# Merch")

st.write("We have a variety of merch available to purchase at our coven. Please feel free to reach out to us at the email provided in the About Us section or through the Facebook group.")

# Add a link to the forum
st.write("Have questions about our merch? Discuss it in our [forum](/?page=Forum)!")


# Get the current file's directory
current_dir = Path(__file__).parent

# Construct the path to the image
patch_path = current_dir / "static" / "patch.png"
bag_path = current_dir / "static" / "bag.png"
sticker1_path = current_dir / "static" / "sticker1.png"
notebook_path = current_dir / "static" / "notebook.png"
sticker2_path = current_dir / "static" / "sticker2.png"


# Display the image
st.write("Patch:")
st.image(str(patch_path))
st.write("Bag:")
st.image(str(bag_path))
st.write("Sticker 1:")
st.image(str(sticker1_path))
st.write("Notebook:")
st.image(str(notebook_path))
st.write("Sticker 2:")
st.image(str(sticker2_path))


