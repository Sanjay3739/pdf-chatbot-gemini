import streamlit as st

def check_auth():
    return st.session_state.get("authenticated", False)

def login_form():
    st.title("🔒 Login Required")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username == "sanjay" and password == "makwana":
            st.session_state["authenticated"] = True
            st.rerun()  # ⬅️ Refresh to load main app
        else:
            st.error("Invalid credentials")
