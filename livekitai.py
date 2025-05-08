import livekit
import os
from dotenv import load_dotenv
import time  

# Load environment variables from .env file
load_dotenv("stark.env")

# Retrieve LiveKit credentials from .env
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_SERVER_URL = os.getenv("LIVEKIT_SERVER_URL")
ROOM_NAME = "stark_ai_room"  # Set a default room name

# Check if API key and server URL are found
if not LIVEKIT_API_KEY or not LIVEKIT_SERVER_URL:
    raise ValueError("Error: LiveKit credentials not found. Please set them in your stark.env file.")

# Initialize LiveKit client
client = livekit.Client(LIVEKIT_SERVER_URL, api_key=LIVEKIT_API_KEY)

def ask_livekit(prompt):
    """Sends user input to LiveKit and returns a response."""
    try:
        room = client.join_room(ROOM_NAME)
        room.send_message(prompt)  # Send user input as a message
        
        # Wait for a response from LiveKit
        response = room.receive_message()  # Adjust based on actual LiveKit implementation
        time.sleep(2)  # Delay for stability
        return response.text.strip()  # Extract and return response text
    except Exception as e:
        return f"LiveKit Error: {str(e)}"

# Test the function in an interactive loop
if __name__ == "__main__":
    print("🤖 LiveKitAI Assistant (Type 'exit' to quit)")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye! 👋")
            break
        response = ask_livekit(user_input)
        print("AI:", response)
