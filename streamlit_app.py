import streamlit as st
import pandas as pd

home_page = st.Page("home_page.py", title="Home", icon="🏠")
about_page = st.Page("about_page.py", title="About", icon="📚")
contact_page = st.Page("contact_page.py", title="Contact Us", icon="📞")
shop_page = st.Page("Shop.py", title="Merch", icon="🛍️")
forum_page = st.Page("forum_page.py", title="Forum", icon="🗣️")
fundraising_page = st.Page("Fundraiser.py", title="Fundraising", icon="💰")

pg = st.navigation([home_page, about_page, contact_page, shop_page, forum_page, fundraising_page])

pg.run()