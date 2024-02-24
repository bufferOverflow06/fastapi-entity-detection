import spacy
import re
from typing import List, Dict, Any
from pydantic import BaseModel

# Load pre-trained SpaCy model
nlp = spacy.load("en_core_web_sm")

# Custom entity patterns using regular expressions
phone_pattern = r'\b(?:\+?(?:91)?|0)?[789]\d{9}\b|\b(?:\+?1\s*(?:[-()]*\d){10})\b|\b\d{3}-\d{4}\b'
email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
age_pattern = r'\b(?:age|AGE)\s*:\s*(\d+)\b'
url_pattern = r'https?://\S+'
blood_group_pattern = r'\b(?:A|B|AB|O)[\s+-]?[rR]?[hH]?[+\-]?(?:ve|Ve|VE|ve|Positive|negative|Negative)\b'
date_pattern = r'\b\d{2}/\d{2}/\d{4}\b|\b\d{4}/\d{2}/\d{2}\b|\b\d{2}/\d{2}/\d{4}\b|\b\d{2}-\d{2}-\d{4}\b'

def extract_entities(sentence):
    try:
        # Process text using SpaCy model
        doc = nlp(sentence)

        # Extract entities recognized by SpaCy
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        # Extract custom entities using regular expressions
        custom_entities = []
        for match in re.finditer(phone_pattern, sentence):
            custom_entities.append((match.group(), "PHONE"))
        
        # Find email matches if they match the email pattern directly
        for match in re.finditer(email_pattern, sentence):
            email_entity = (match.group(), "EMAIL")
            custom_entities.append(email_entity)

        for match in re.finditer(age_pattern, sentence):
            custom_entities.append((match.group(1), "AGE"))

        for match in re.finditer(url_pattern, sentence):
            custom_entities.append((match.group(), "URL"))

        for match in re.finditer(date_pattern, sentence):
            custom_entities.append((match.group(), "DATE"))
            
        # Find unrecognized words and mark them as "OTHER"
        for token in doc:
            if token.text not in [ent[0] for ent in entities] and not re.search(phone_pattern, token.text) and not re.search(email_pattern, token.text) and not re.search(age_pattern, token.text) and not re.search(url_pattern, token.text) and not re.search(date_pattern, token.text) and token.is_alpha:
                custom_entities.append((token.text, "OTHER"))

        # Combine standard and custom entities
        entities += custom_entities

        return entities
    except Exception as e:
        print(f"Error: {e}")
        return []

# Pydantic model for input data validation
class InputData(BaseModel):
    sentences: List[str]

# Pydantic model for output data validation
class OutputData(BaseModel):
    entities: List[Dict[str, Any]]
