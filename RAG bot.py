import streamlit as st
import requests

# Constants
BASE_API_URL = "http://127.0.0.1:7861"
FLOW_ID = "3b598af9-54c9-40f6-a30e-074ba9f07102"
ENDPOINT = "" # You can set a specific endpoint name in the flow settings

# Function to run the flow
def run_flow(message: str) -> dict:
    """
    Run a flow with a given message.

    :param message: The message to send to the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{ENDPOINT or FLOW_ID}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    response = requests.post(api_url, json=payload)
    return response.json()

# Function to extract the desired message
def extract_message(response: dict) -> str:
    try:
        # Navigate to the message inside the response structure
        return response['outputs'][0]['outputs'][0]['results']['message']['text']
    except (KeyError, IndexError):
        return "No valid message found in response."

# Streamlit App
def main():
    st.title("Langflow Chatbot 🤖")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages with avatars
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    # Input box for user message
    if query := st.chat_input("Ask me anything..."):
        # Add user message to session state
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query,
                "avatar": "💬",  # Emoji for user
            }
        )
        with st.chat_message("user", avatar="💬"):  # Display user message
            st.write(query)

        # Call the Langflow API and get the assistant's response
        with st.chat_message("assistant", avatar="🤖"):  # Emoji for assistant
            message_placeholder = st.empty()  # Placeholder for assistant response
            with st.spinner("Thinking..."):
                # Fetch response from Langflow
                assistant_response = extract_message(run_flow(query))
                message_placeholder.write(assistant_response)

        # Add assistant response to session state
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_response,
                "avatar": "🤖",  # Emoji for assistant
            }
        )

if __name__ == "__main__":
    main()