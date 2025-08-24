#!/usr/bin/env python3
"""
Test script for the Text Anonymizer API
"""
import requests
import json

def test_api():
    """Test the anonymizer API with sample text"""
    base_url = "http://localhost:8000"

    # Test data
    test_cases = [
        {
            "name": "Basic entities",
            "text": "Hello, my name is John Doe and I live in New York. I work at Google."
        },
        {
            "name": "Multiple persons and locations",
            "text": "Sarah Johnson from London met with Michael Smith from Microsoft in Seattle."
        },
        {
            "name": "Mixed entities",
            "text": "The CEO of Apple, Tim Cook, announced the new iPhone at the Apple Park in Cupertino, California."
        },
        {
            "name": "No entities",
            "text": "This is a simple sentence without any named entities to detect."
        }
    ]

    print("Testing Text Anonymizer API")
    print("=" * 50)

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.json()}")
        print()
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to the API. Make sure it's running on localhost:8000")
        return

    # Test anonymization
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"Original: {test_case['text']}")

        try:
            response = requests.post(
                f"{base_url}/anonymize",
                headers={"Content-Type": "application/json"},
                data=json.dumps({"text": test_case["text"]})
            )

            if response.status_code == 200:
                result = response.json()
                print(f"Anonymized: {result['anonymized_text']}")
                print(f"Entities found: {len(result['entities_found'])}")

                for entity in result['entities_found']:
                    print(f"  - {entity['entity']} -> {entity['token']} (confidence: {entity['confidence']})")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"Error testing case: {e}")

        print("-" * 50)

if __name__ == "__main__":
    test_api()
