import streamlit as st
import requests

# Define Streamlit app
st.title("Entity Extraction Using FastAPI")

# Text input field for user input
text_input = st.text_area("Enter text to extract entities:")

# Function to handle button click
def extract_entities(text):
    # API endpoint
    api_endpoint = "https://fastapi-entity-detection-1.onrender.com/extract_entities"
    
    # Prepare data as JSON
    data = {"sentences": [text]}
    
    # Send POST request to API endpoint
    response = requests.post(api_endpoint, json=data)
    
    # Check if request was successful
    if response.status_code == 200:
        # Get response JSON
        response_json = response.json()
        
        # Display extracted entities
        entities = response_json.get("entities", [])
        for entity in entities:
            sentence = entity.get("sentence", "")
            extracted_entities = entity.get("entities", [])
            st.write(f"Entities in sentence: {sentence}")
            for ent_text, ent_type in extracted_entities:
                st.write(f"- {ent_text} ({ent_type})")
    else:
        st.error("Error occurred while extracting entities. Please try again.")

# Button to trigger entity extraction
if st.button("Extract Entities"):
    if text_input:
        extract_entities(text_input)
    else:
        st.warning("Please enter some text before extracting entities.")
