import streamlit as st
import pandas as pd

home_page = st.Page("home_page.py", title="Home", icon="🏠")
about_page = st.Page("about_page.py", title="About", icon="📚")
contact_page = st.Page("contact_page.py", title="Contact Us", icon="📞")

pg = st.navigation([home_page, about_page, contact_page])

pg.run()

