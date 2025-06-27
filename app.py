# ==============================================================================
# FILE: app.py
# PURPOSE: Main application file for the AI Email Generator.
# ==============================================================================

# 1. IMPORT LIBRARIES
# -------------------
# We import Streamlit for the web UI, Google Generative AI for the AI model,
# and OS for interacting with environment variables (our API key).
import streamlit as st
import google.generativeai as genai
import os

# 2. CONFIGURE THE PAGE AND API KEY
# ---------------------------------
# Set the title and icon that appear in the browser tab.
st.set_page_config(
    page_title="Gemini Email Generator",
    page_icon="📧",
    layout="centered"
)

# This is the most important part for deployment.
# We try to get the API key from Streamlit's secret management.
# This is secure and the recommended way for deployed apps.
try:
    # This line will work when you deploy on Streamlit Community Cloud
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    # This part is for local development if you want to run it on your own computer.
    # It tells you that you need to set up your secrets for deployment.
    st.error("API Key not found. Please add your GOOGLE_API_KEY to the Streamlit secrets.")
    st.stop() # Stop the app if the key is not found.


# 3. DEFINE THE AI FUNCTION
# -------------------------
# This function will take user input and send it to the Gemini API.
def generate_email(recipient, sender, purpose, tone, key_points):
    """
    Uses the Gemini API to generate an email based on provided details.
    """
    # Initialize the Gemini model. 'gemini-1.5-flash' is fast and efficient.
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Create a detailed prompt to guide the AI. This is called "prompt engineering".
    # A good prompt gives much better results.
    prompt_template = f"""
    You are a professional email writing assistant. Your task is to generate a high-quality email.

    **Email Details:**
    - **To:** {recipient}
    - **From:** {sender}
    - **Tone:** {tone}
    - **Purpose:** {purpose}
    - **Key Points to Include:**
    {key_points}

    **Instructions:**
    1. Generate a relevant and concise subject line. Do not use a placeholder like "[Subject]".
    2. Write the email body, making sure it flows well and incorporates all key points.
    3. The email should start with a proper greeting and end with an appropriate closing.
    4. The final output must be ONLY the email (Subject, Body, Closing). Do not add any extra notes.

    **Generated Email:**
    """

    # Call the API to generate content
    try:
        response = model.generate_content(prompt_template)
        return response.text
    except Exception as e:
        # Handle potential errors from the API
        return f"An error occurred: {e}"


# 4. CREATE THE STREAMLIT USER INTERFACE
# ---------------------------------------
st.title("📧 AI Email Generator")
st.write("Fill in the details below to have Gemini AI craft your email.")

# Use a form to group inputs and have a single "Generate" button.
with st.form("email_generator_form"):
    st.header("Email Information")

    # Create two columns for a cleaner layout
    col1, col2 = st.columns(2)
    with col1:
        sender_name = st.text_input("Your Name", placeholder="e.g., Jane Doe")
    with col2:
        recipient_name = st.text_input("Recipient's Name", placeholder="e.g., John Smith")

    purpose = st.text_input("What is the purpose of this email?", placeholder="e.g., Follow up on our recent meeting")

    tone = st.selectbox(
        "Select the desired tone:",
        ("Professional", "Friendly", "Formal", "Casual", "Urgent")
    )

    key_points = st.text_area(
        "What key points should be included? (one per line)",
        height=150,
        placeholder="- Thank them for their time\n- Confirm the agreed-upon project deadline\n- Ask for the meeting notes"
    )

    # The submit button for the form
    submit_button = st.form_submit_button("✨ Generate Email")


# 5. HANDLE FORM SUBMISSION
# -------------------------
# This code runs only when the user clicks the "Generate Email" button.
if submit_button:
    # Basic check to ensure fields are not empty
    if not all([sender_name, recipient_name, purpose, key_points]):
        st.warning("Please fill in all the fields.")
    else:
        # Show a "spinner" message while the AI is working
        with st.spinner("Generating your email..."):
            generated_email = generate_email(
                recipient=recipient_name,
                sender=sender_name,
                purpose=purpose,
                tone=tone,
                key_points=key_points
            )
            st.success("Email generated!")

            # Display the generated email in a nice, copyable format
            st.subheader("Your Generated Email:")
            st.text_area("You can copy the text below", generated_email, height=300)
