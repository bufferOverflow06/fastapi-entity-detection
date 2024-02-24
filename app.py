from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from model import extract_entities, InputData, OutputData

app = FastAPI()

# FastAPI route to process input and return entities
@app.post("/extract_entities", response_model=OutputData)
async def process_sentences(data: InputData):
    entities_list = []
    for sentence in data.sentences:
        entities = extract_entities(sentence)
        entities_list.append({"sentence": sentence, "entities": entities})
    return {"entities": entities_list}