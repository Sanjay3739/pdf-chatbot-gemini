import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get USER_NAME key and PASSWORD from the environment variables
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")

# Check if the user is authenticated
def check_auth():
    """
    Checks if the user is authenticated based on session state.
    Returns True if authenticated, False otherwise.
    """
    return st.session_state.get("authenticated", False)

# Display the login form and handle user authentication
def login_form():
    """
    Displays the login form and handles user authentication.
    If the credentials are correct, updates the session state to authenticated.
    """
    st.title("🔒 Login Required")
    
    # Username and password input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Login button
    login_btn = st.button("Login")

    # Check if the user clicks the login button
    if login_btn:
        if username == USER_NAME and password == PASSWORD:
            # Store authentication status in session state
            st.session_state["authenticated"] = True
            st.success("Login successful!")
            st.rerun()  # Refresh to load the main app
        else:
            st.error("Invalid credentials. Please try again.")

# Check if the user is authenticated before proceeding with the app
def authenticate():
    """
    If the user is not authenticated, displays the login form and stops further execution.
    """
    if not check_auth():
        login_form()
        st.stop()  # Stop further execution if not authenticated
