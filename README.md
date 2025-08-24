# Text Anonymizer API

A FastAPI-based text anonymizer that uses Named Entity Recognition (NER) to redact sensitive information from text by replacing entities with tokens like `[PERSON]`, `[LOCATION]`, etc.

## Features

- **Named Entity Recognition**: Uses Hugging Face transformers with BERT model fine-tuned on CoNLL-03 dataset
- **Entity Replacement**: Replaces detected entities with standardized tokens:
  - `[PERSON]` for person names
  - `[LOCATION]` for locations
  - `[ORGANIZATION]` for organizations
  - `[MISCELLANEOUS]` for other entities
- **RESTful API**: Simple POST endpoint for text anonymization
- **Docker Support**: Ready-to-deploy Docker container
- **Health Checks**: Built-in health check endpoints

## Installation

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd anonymizer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t text-anonymizer .
```

2. Run the container:
```bash
docker run -p 8000:8000 text-anonymizer
```

## API Usage

### Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /anonymize` - Anonymize text

### Example Request

```bash
curl -X POST "http://localhost:8000/anonymize" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, my name is John Doe and I live in New York. I work at Google."}'
```

### Example Response

```json
{
  "original_text": "Hello, my name is John Doe and I live in New York. I work at Google.",
  "anonymized_text": "Hello, my name is [PERSON] and I live in [LOCATION]. I work at [ORGANIZATION].",
  "entities_found": [
    {
      "entity": "John Doe",
      "label": "PER",
      "token": "[PERSON]",
      "confidence": 0.9998,
      "start": 18,
      "end": 26
    },
    {
      "entity": "New York",
      "label": "LOC",
      "token": "[LOCATION]",
      "confidence": 0.9995,
      "start": 42,
      "end": 50
    },
    {
      "entity": "Google",
      "label": "ORG",
      "token": "[ORGANIZATION]",
      "confidence": 0.9994,
      "start": 62,
      "end": 68
    }
  ]
}
```

## API Documentation

Once the application is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative documentation: `http://localhost:8000/redoc`

## Model Information

This application uses the `dbmdz/bert-large-cased-finetuned-conll03-english` model from Hugging Face, which is a BERT model fine-tuned for Named Entity Recognition on the CoNLL-03 dataset. It can identify:

- **PER/PERSON**: Person names
- **LOC/LOCATION**: Locations (cities, countries, etc.)
- **ORG/ORGANIZATION**: Organizations (companies, institutions, etc.)
- **MISC/MISCELLANEOUS**: Other named entities

## Security Considerations

- The application runs as a non-root user in the Docker container
- Input validation is performed on all endpoints
- No sensitive data is logged
- The model processes text locally without external API calls

## Performance Notes

- The model is loaded once at startup to avoid repeated loading
- First request might be slower due to model initialization
- Subsequent requests are much faster
- Consider using GPU for better performance with large texts

## License

This project is open source. Please check the licenses of the dependencies, especially the Hugging Face model being used.
