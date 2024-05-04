## loading all the environment variables
from dotenv import load_dotenv
load_dotenv() 

import streamlit as st
import os
import google.generativeai as genai

# Set up Google API key
os.environ["GOOGLE_API_KEY"] = "your_google_api_key_here"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Placeholder for the fine-tuned model response function
def get_fine_tuned_response(question):
    # Placeholder for the fine-tuned model response
    return ["Fine-tuned model response placeholder"]

##initialize our streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Text input for user query
input_text = st.text_input("Input: ", key="input_text")

# Button to submit the query
submit_button = st.button("Ask the question")

if submit_button and input_text:
    # Get response from the fine-tuned model
    response = get_fine_tuned_response(input_text)
    
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input_text))
    st.subheader("The Response is")
    
    # Display the response
    for chunk in response:
        st.write(chunk)
        st.session_state['chat_history'].append(("Bot", chunk))

# Display the chat history
st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")