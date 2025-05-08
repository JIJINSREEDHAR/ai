import openai
import os
from dotenv import load_dotenv
import time  

# Load environment variables from .env file
load_dotenv("stark.env")

# Retrieve the OpenAI API key from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if API key is found
if not OPENAI_API_KEY:
    raise ValueError("Error: OpenAI API key not found. Please set it in your .env file.")

# ✅ Correct way to initialize OpenAI client
client = openai.Client()

def ask_openai(prompt):
    """Sends user input to OpenAI and returns a detailed response."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # ✅ Free-tier model
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,  
            temperature=0.7,  
            top_p=0.9  
        )
        time.sleep(2)  # ✅ Delay to avoid rate limits
        return response.choices[0].message.content.strip()
    except openai.RateLimitError:
        return "OpenAI API Error: Rate limit exceeded. Try again later."
    except openai.AuthenticationError:
        return "OpenAI API Error: Invalid API key. Check your OpenAI API key in stark.env."
    except openai.OpenAIError as e:
        return f"OpenAI API Error: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# Test the function in an interactive loop
if __name__ == "__main__":
    print("🤖 OpenAI Assistant (Type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye! 👋")
            break
        response = ask_openai(user_input)
        print("AI:", response)
