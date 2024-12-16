from dotenv import load_dotenv
from PIL import Image
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load image (with error handling)
try:
    image = Image.open('yuu.png')
except FileNotFoundError:
    image = None  # Handle case if the image is not found

# Initialize the Gemini Pro model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Streamlit page configuration
st.set_page_config(page_title="Yuu")
if image:
    st.image(image, width=200)
st.header("Chat with Yuu")

# Initialize chat history in session state if not already initialized
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input box for user
input_text = st.text_input("Input: ", key="input")
output_text = ""
history = ""

# Submit button
submit = st.button("Send")

# Function to get a response from Gemini Pro
def get_gemini_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error while contacting Gemini API: {e}")
        return []

if submit and input_text:
    # Add user query to chat history
    st.session_state['chat_history'].append(("You", input_text))

    # Prepare the context from the chat history
    context = "Context: You have to act as a cute therapist chatting friend named 'Yuu'. Respond thoughtfully, considering the chat history. Here's the past chat history just for context:\n"
    for role, text in st.session_state['chat_history']:
        context += f"{role}: {text}\n"
    
    # Get the response from Gemini Pro
    response = get_gemini_response(context + "User: " + input_text)
    
    # Concatenate chunks into a single paragraph
    output_text = ''.join([chunk.text for chunk in response])  # Combine all chunks

    # Display the response as a paragraph
    st.subheader("The Response is")
    st.write(output_text)

    # Add Yuu's response to the history
    st.session_state['chat_history'].append(("Yuu", output_text))

# Display the chat history
st.subheader("Chat History:")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
