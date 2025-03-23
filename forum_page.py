import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime


st.markdown("# Forum")
st.sidebar.markdown("# Forum")

# Initialize session state for messages if it doesn't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Database connection
def init_db():
    db_path = "static/forum.db"
    
    # Check if the database file exists and is valid
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA integrity_check;")  # Check database integrity
        except sqlite3.DatabaseError:
            # If the file is invalid, delete it and create a new one
            conn.close()
            os.remove(db_path)
            conn = sqlite3.connect(db_path)
    else:
        conn = sqlite3.connect(db_path)

    # Create the forum_messages table if it doesn't exist
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forum_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn

conn = init_db()

# Load messages from the database into session state
def load_messages():
    cursor = conn.cursor()
    cursor.execute("SELECT message, timestamp FROM forum_messages ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    st.session_state.messages = [
        {"name": "User", "message": row[0], "timestamp": row[1]} for row in rows
    ]

# Initialize session state with messages from the database
if 'messages' not in st.session_state or not st.session_state.messages:
    load_messages()

# Define admin username
ADMIN_USERNAME = "admin"

# Admin credentials (for simplicity, hardcoded here)
ADMIN_CREDENTIALS = {"username": "admin", "password": "Joe0606"}

# Login state
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "show_login_form" not in st.session_state:
    st.session_state.show_login_form = False

# Show login button if no user is logged in
if st.session_state.current_user is None:
    if not st.session_state.show_login_form:
        if st.button("Login"):
            st.session_state.show_login_form = True
    else:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Login")

            if login_submitted:
                if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
                    st.session_state.current_user = username
                    st.session_state.show_login_form = False
                    st.success("Logged in as admin!")
                else:
                    st.error("Invalid username or password.")
else:
    st.sidebar.write(f"Logged in as: {st.session_state.current_user}")
    if st.sidebar.button("Logout"):
        st.session_state.current_user = None
        st.session_state.show_login_form = False

# Form for new message
with st.form("new_message", clear_on_submit=True):
    user_name = st.text_input("Your Name")
    message = st.text_area("Your Message")
    submitted = st.form_submit_button("Post Message")

    if submitted and user_name and message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Save message to database
        conn.execute(
            "INSERT INTO forum_messages (user_id, message, timestamp) VALUES (?, ?, ?)",
            (1, message, timestamp)  # Assuming user_id is 1 for now
        )
        conn.commit()
        # Update session state
        st.session_state.messages.insert(0, {
            "name": user_name,
            "message": message,
            "timestamp": timestamp
        })

# Display messages
st.subheader("Messages")
for idx, msg in enumerate(st.session_state.messages):
    st.text(f"{msg['timestamp']} - {msg['name']}:")
    st.write(msg['message'])
    
    # Allow editing and deleting if the user is admin
    if st.session_state.get("current_user") == ADMIN_USERNAME:
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Edit Message {idx + 1}", key=f"edit_{idx}"):
                new_message = st.text_area("Edit Message", value=msg['message'], key=f"edit_area_{idx}")
                if st.button(f"Save Changes {idx + 1}", key=f"save_{idx}"):
                    # Update the database
                    conn.execute(
                        "UPDATE forum_messages SET message = ? WHERE timestamp = ? AND message = ?",
                        (new_message, msg['timestamp'], msg['message'])
                    )
                    conn.commit()
                    # Update session state
                    st.session_state.messages[idx]['message'] = new_message
                    st.success("Message updated successfully!")
        with col2:
            if st.button(f"Delete Message {idx + 1}", key=f"delete_{idx}"):
                # Delete the message from the database
                conn.execute(
                    "DELETE FROM forum_messages WHERE timestamp = ? AND message = ?",
                    (msg['timestamp'], msg['message'])
                )
                conn.commit()
                # Remove the message from session state
                del st.session_state.messages[idx]
                st.success("Message deleted successfully!")
                break  # Exit the loop to avoid index issues after deletion
    
    st.markdown("---")

# Option to download messages as CSV
if st.button("Download Messages as CSV"):
    df = pd.DataFrame(st.session_state.messages)
    csv = df.to_csv(index=False)
    st.download_button(
        label="Click here to download",
        data=csv,
        file_name="forum_messages.csv",
        mime="text/csv",
    )