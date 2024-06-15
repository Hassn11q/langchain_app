import streamlit as st
import requests

def get_llm_response(input_text):
    try:
        # Define the payload according to the API schema
        payload = {
            "input": input_text,
            "config": {},
            "kwargs": {}
        }
        # Use the Render URL
        response = requests.post("https://langchain-app-8xsr.onrender.com/chatbot/invoke", json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the JSON response
        response_json = response.json()
        
        # Check and return the expected 'output' key from the response
        if "output" in response_json:
            return response_json["output"]
        else:
            return "Error: 'output' key not found in the response"
    except requests.exceptions.RequestException as e:
        return f"Connection error: {e}"

# Streamlit input and output

st.title("misbah chatbot")
input_text = st.text_input("Enter your text:")
if input_text:
    st.write(get_llm_response(input_text))
