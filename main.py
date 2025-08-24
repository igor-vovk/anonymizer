from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import re
import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Text Anonymizer API",
    description="Anonymize text using Named Entity Recognition to replace sensitive information with tokens",
    version="1.0.0"
)

# Pydantic models
class TextInput(BaseModel):
    text: str

class AnonymizedResponse(BaseModel):
    original_text: str
    anonymized_text: str
    entities_found: List[Dict[str, Any]]

# Global variables for the NER model
ner_pipeline = None
tokenizer = None
model = None

@app.on_event("startup")
async def load_model():
    """Load the NER model on startup"""
    global ner_pipeline, tokenizer, model
    try:
        logger.info("Loading NER model...")
        model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForTokenClassification.from_pretrained(model_name)

        ner_pipeline = pipeline(
            "ner",
            model=model,
            tokenizer=tokenizer,
            aggregation_strategy="simple"
        )

        logger.info("NER model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load NER model: {str(e)}")
        raise e

def anonymize_text(text: str) -> tuple[str, List[Dict[str, str]]]:
    """
    Anonymize text by replacing named entities with tokens

    Args:
        text: Input text to anonymize

    Returns:
        Tuple of (anonymized_text, entities_found)
    """
    if not ner_pipeline:
        raise HTTPException(status_code=500, detail="NER model not loaded")

    try:
        # Get entities from the text
        entities = ner_pipeline(text)

        # Sort entities by start position in reverse order to avoid index shifting
        entities = sorted(entities, key=lambda x: x['start'], reverse=True)

        anonymized_text = text
        entities_found = []

        # Entity label mapping to tokens
        entity_tokens = {
            'PER': '[PERSON]',
            'PERSON': '[PERSON]',
            'LOC': '[LOCATION]',
            'LOCATION': '[LOCATION]',
            'ORG': '[ORGANIZATION]',
            'ORGANIZATION': '[ORGANIZATION]',
            'MISC': '[MISCELLANEOUS]',
            'MISCELLANEOUS': '[MISCELLANEOUS]'
        }

        for entity in entities:
            label = entity['entity_group']
            start = entity['start']
            end = entity['end']
            word = entity['word']
            confidence = entity['score']

            # Get the token for this entity type
            token = entity_tokens.get(label, f'[{label}]')

            # Replace the entity in the text
            anonymized_text = anonymized_text[:start] + token + anonymized_text[end:]

            entities_found.append({
                'entity': word,
                'label': label,
                'token': token,
                'confidence': float(confidence),
                'start': int(start),
                'end': int(end)
            })

        return anonymized_text, entities_found

    except Exception as e:
        logger.error(f"Error during anonymization: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Anonymization failed: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Text Anonymizer API",
        "description": "Use POST /anonymize to anonymize text",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_status = "loaded" if ner_pipeline is not None else "not loaded"
    return {
        "status": "healthy",
        "model_status": model_status
    }

@app.post("/anonymize", response_model=AnonymizedResponse)
async def anonymize_endpoint(input_data: TextInput):
    """
    Anonymize text by replacing named entities with tokens

    Args:
        input_data: JSON with 'text' field containing the text to anonymize

    Returns:
        JSON with original text, anonymized text, and found entities
    """
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        anonymized_text, entities_found = anonymize_text(input_data.text)

        return AnonymizedResponse(
            original_text=input_data.text,
            anonymized_text=anonymized_text,
            entities_found=entities_found
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
