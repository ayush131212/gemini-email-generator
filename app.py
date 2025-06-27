# ==============================================================================
# AI EMAIL GENERATOR - app.py
# ==============================================================================
# This application uses Streamlit for the web interface and the Google Gemini
# API for email generation.
#
# To run locally:
# 1. Make sure you have a .env file with your GOOGLE_API_KEY
#    (e.g., GOOGLE_API_KEY="your_key_here")
# 2. In your terminal, run: streamlit run app.py
# ==============================================================================

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Email Generator",
    page_icon="📧",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- API KEY CONFIGURATION ---
# This function handles loading the API key securely.
# It first tries Streamlit's secrets management (for deployment)
# and falls back to a local .env file (for development).
def load_api_key():
    try:
        # Ideal for Streamlit Community Cloud deployment
        genai.configure(api_key=st.secrets["AIzaSyBW56boEAbSgHllcnJW0xlG3DEaeE4MU90"])
        st.sidebar.success("API key loaded from Streamlit secrets.", icon="✅")
    except (KeyError, FileNotFoundError):
        # Fallback for local development
        try:
            load_dotenv()  # Load environment variables from .env file
            api_key = os.getenv("AIzaSyBW56boEAbSgHllcnJW0xlG3DEaeE4MU90")
            if not api_key:
                st.sidebar.error("API key not found in .env file.", icon="❌")
                st.stop()
            genai.configure(api_key=api_key)
            st.sidebar.success("API key loaded from .env file.", icon="✅")
        except Exception as e:
            st.sidebar.error(f"Could not load API key: {e}", icon="❌")
            st.stop()

load_api_key()

# --- MODEL AND FUNCTION ---
# Initialize the Generative Model
# Using 'gemini-1.5-flash' for its speed and capability. 'gemini-pro' is also an option.
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_email(recipient_name, sender_name, purpose, tone, key_points):
    """
    Generates an email using the Gemini API based on user inputs.
    """
    # A detailed prompt that instructs the model on how to behave.
    prompt = f"""
    As an expert email writing assistant, your task is to craft a professional and effective email.

    **Instructions:**
    1.  Create a clear, relevant, and compelling subject line. Do not use placeholders like "[Subject]".
    2.  The email must be addressed to `{recipient_name}` and signed by `{sender_name}`.
    3.  The tone of the email must be `{tone}`.
    4.  The core purpose is: "{purpose}".
    5.  You must seamlessly integrate the following key points into the email body:
        ```
        {key_points}
        ```
    6.  Ensure the final output is only the email itself (Subject, Body, Closing), with no extra commentary or notes.

    **GENERATE THE EMAIL NOW**
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating the email: {e}"



st.title("📧 AI Email Generator")
st.write("Fill in the details below and let Gemini draft the perfect email for you.")

# Create a form for a cleaner user experience
with st.form("email_form"):
    st.header("Email Details")

    col1, col2 = st.columns(2)
    with col1:
        sender_name = st.text_input("Your Name", placeholder="e.g., Alex Johnson")
    with col2:
        recipient_name = st.text_input("Recipient's Name", placeholder="e.g., Dr. Maria Garcia")

    purpose = st.text_input("Purpose of the Email", placeholder="e.g., Request for a recommendation letter")

    tone_options = ["Formal", "Professional", "Friendly", "Casual", "Urgent", "Persuasive"]
    tone = st.selectbox("Select the Desired Tone", tone_options)

    key_points = st.text_area(
        "Key Points to Include (one per line)",
        height=150,
        placeholder="- Mention my performance in your class last semester\n- Applying for the Master's in Data Science program\n- The application deadline is next Friday"
    )

    # Submit button for the form
    submitted = st.form_submit_button("✨ Generate Email")

# --- GENERATE AND DISPLAY EMAIL ---

if submitted:
    # Basic validation
    if not all([sender_name, recipient_name, purpose, key_points]):
        st.warning("Please fill in all the fields before generating.", icon="⚠️")
    else:
        with st.spinner("Your email is being crafted by AI..."):
            generated_email = generate_email(recipient_name, sender_name, purpose, tone, key_points)
            st.success("Email Generated Successfully!", icon="🎉")

            st.subheader("Here's Your Draft:")
            # Use a text area to display the result, making it easy to copy
            st.text_area("Generated Email", generated_email, height=300)

st.sidebar.header("About")
st.sidebar.info(
    "This tool uses the Google Gemini API to generate emails based on your input. "
    "Remember to always review and edit the generated content to ensure it perfectly fits your needs."
)
