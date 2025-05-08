import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv("stark.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Check if API key is found
if not OPENAI_API_KEY:
    raise ValueError("Error: OpenAI API key not found. Please set it in your .env file.")

# Initialize OpenAI client
client = openai.Client(api_key=OPENAI_API_KEY)

# List available models
try:
    models = client.models.list()
    print([model.id for model in models.data])
except openai.AuthenticationError:
    print("🚨 Invalid API key! Check your OpenAI API key in the .env file.")
