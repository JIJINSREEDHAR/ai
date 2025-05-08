import os
from dotenv import load_dotenv
import time
import requests

# Load environment variables from .env file
load_dotenv("stark.env")

# Retrieve the DeepSeek API key from .env
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Check if API key is found
if not DEEPSEEK_API_KEY:
    raise ValueError("Error: DeepSeek API key not found. Please set it in your .env file.")

# DeepSeek API endpoint
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Replace with the actual API endpoint

def ask_deepseek(prompt):
    """Sends user input to DeepSeek and returns a detailed response."""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-model-name",  # Replace with the specific DeepSeek model
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()  # Adjust based on DeepSeek's response structure
    except requests.exceptions.RequestException as e:
        return f"DeepSeek API Error: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Test the function in an interactive loop
if __name__ == "__main__":
    print(" DeepSeek Assistant (Type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye! ")
            break
        response = ask_deepseek(user_input)
        print("AI:", response)