"""
Example usage of the Text Anonymizer API
"""

# Example 1: Using requests library
import requests
import json

def example_with_requests():
    url = "http://localhost:8000/anonymize"

    # Sample text with various entities
    text = """
    Dear Mr. John Smith,

    Thank you for your interest in our company, TechCorp Inc., located in San Francisco, California.
    We received your application for the Software Engineer position.

    Please contact our HR manager, Sarah Johnson, at our New York office for further details.
    You can also reach out to our London branch where Michael Brown is the regional director.

    We look forward to hearing from you.

    Best regards,
    Alice Williams
    Recruitment Team
    """

    payload = {"text": text}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            result = response.json()

            print("Original Text:")
            print("-" * 50)
            print(result["original_text"])

            print("\nAnonymized Text:")
            print("-" * 50)
            print(result["anonymized_text"])

            print(f"\nEntities Found ({len(result['entities_found'])}):")
            print("-" * 50)
            for entity in result["entities_found"]:
                print(f"• {entity['entity']} → {entity['token']} (confidence: {entity['confidence']:.4f})")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API. Make sure the server is running on localhost:8000")
    except Exception as e:
        print(f"Error: {e}")

# Example 2: Using curl command (for reference)
def example_curl_commands():
    print("\n" + "="*60)
    print("CURL COMMAND EXAMPLES")
    print("="*60)

    examples = [
        {
            "name": "Simple example",
            "text": "Hello, I am John Doe from New York working at Google."
        },
        {
            "name": "Multiple entities",
            "text": "Microsoft CEO Satya Nadella visited the Seattle headquarters with Tim Cook from Apple."
        }
    ]

    for example in examples:
        print(f"\n{example['name']}:")
        print("-" * 30)
        curl_cmd = f'''curl -X POST "http://localhost:8000/anonymize" \\
     -H "Content-Type: application/json" \\
     -d '{{"text": "{example['text']}"}}'
'''
        print(curl_cmd)

if __name__ == "__main__":
    print("Text Anonymizer API - Usage Examples")
    print("="*50)

    # Run the requests example
    example_with_requests()

    # Show curl examples
    example_curl_commands()

    print("\n" + "="*60)
    print("ADDITIONAL ENDPOINTS")
    print("="*60)
    print("Health check: GET http://localhost:8000/health")
    print("API info: GET http://localhost:8000/")
    print("Documentation: http://localhost:8000/docs")
    print("Alternative docs: http://localhost:8000/redoc")
