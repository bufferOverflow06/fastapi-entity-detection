from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from model import extract_entities, InputData, OutputData
from fastapi.responses import HTMLResponse

app = FastAPI()

# Define route for the root URL
@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <html>
    <head>
        <title>Text Extraction Using FastAPI</title>
    </head>
    <body>
        <h1>Welcome to Text Extraction Using FastAPI</h1>
        <p>This is a FastAPI application for extracting entities from text using a pre-trained SpaCy model.</p>
        <h2>How It Works</h2>
        <p>To extract entities, send a POST request to the /extract_entities endpoint with a JSON payload containing the text data.</p>
        <p>The application will process the input text using a pre-trained SpaCy model to identify entities such as names, dates, organizations, and more.</p>
        <h2>API Endpoint</h2>
        <p>Endpoint: POST /extract_entities</p>
        <p>Request Body: {"sentences": ["Text sentence 1", "Text sentence 2", ...]}</p>
        <p>Response: {"entities": [{"sentence": "Text sentence 1", "entities": [...]}]}</p>
        <h2>GitHub Repository</h2>
        <p>You can find the source code for this project on GitHub: <a href="https://github.com/bufferOverflow06/fastapi-entity-detection.git">FastAPI Entity Detection Repository</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# FastAPI route to process input and return entities
@app.post("/extract_entities", response_model=OutputData)
async def process_sentences(data: InputData):
    entities_list = []
    for sentence in data.sentences:
        entities = extract_entities(sentence)
        entities_list.append({"sentence": sentence, "entities": entities})
    return {"entities": entities_list}