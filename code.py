import streamlit as st
import openai
import os

# Initialize the Streamlit app
st.title("AI Chatbot with OpenAI")

# Securely handle OpenAI API Key
if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = None

def set_api_key():
    if st.session_state.api_key_input:
        st.session_state.openai_api_key = st.session_state.api_key_input
        st.success("API Key set successfully!")

if not st.session_state.openai_api_key:
    with st.sidebar.expander("Set API Key"):
        st.text_input("Enter your OpenAI API Key", type="password", key="api_key_input")
        st.button("Save API Key", on_click=set_api_key)
    st.warning("Please set your OpenAI API Key to continue.")
    st.stop()

# Sidebar configuration
st.sidebar.title("Chatbot Settings")
model = st.sidebar.selectbox("Model", ["gpt-4", "gpt-3.5-turbo"])
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=500, value=150)
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Bot:** {message['content']}")

# Input box for user
user_input = st.text_input("Your message:")
if st.button("Send") and user_input.strip():
    # Add the user input to the chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenAI API
    try:
        response = openai.ChatCompletion.create(
            api_key=st.session_state.openai_api_key,
            model=model,
            messages=st.session_state.messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # Get the assistant's reply
        assistant_message = response["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        # Display the assistant's reply
        st.write(f"**Bot:** {assistant_message}")

    except Exception as e:
        st.error(f"An error occurred: {e}")
