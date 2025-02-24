import pyttsx3
import speech_recognition as sr
import time
from openpyxl import * #load workbook in Excel
import random

# Initialize recognizer
r = sr.Recognizer()
keywords = ["stark", "hey stark", "hello", "hi", "hey", "get ready"]  # Wake words

# Function to make the system speak
def Speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('voice', engine.getProperty('voices')[0].id)
    engine.say(text)
    engine.runAndWait()

# Callback function for wake word detection
def callback(recognizer, audio):
    try:
        speech_as_text = recognizer.recognize_google(audio).lower()  # Using Google Speech Recognition
        print(f"Heard: {speech_as_text}")

        if any(word in speech_as_text for word in keywords):
            Speak("Yes, I am ready!")
            recognize_main()  # Now safely starts main recognition

    except sr.UnknownValueError:
        print("Didn't catch that.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Function to process user commands
def recognize_main():
    try:
        with sr.Microphone() as source:
            print("Say something!")
            r.adjust_for_ambient_noise(source)  # Reduce noise
            audio = r.listen(source)

        data = r.recognize_google(audio).lower()
        print("You said: " + data)

        if "how are you" in data:
            Speak("I'm doing well, thank you!")
        elif "hello" in data or "hi" in data or "hey" in data:
            Speak("Hello! How can I help?")
        elif "get ready" in data:
            Speak("Getting ready for action!")
        else:
            Speak("I'm sorry, I didn't understand that.")

    except sr.UnknownValueError:
        print("Stark did not understand your request.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

# Function to start the background listener
def start_recognizer():
    print("Waiting for a keyword... 'Stark', 'Hey Stark', 'Hello', 'Hi', 'Hey', or 'Get Ready'")
    mic = sr.Microphone()
    
    with mic as source:
        r.adjust_for_ambient_noise(source)  # Reduce background noise

    stop_listening = r.listen_in_background(mic, callback)  # Start listening
    return stop_listening

# Start the recognizer and keep the program running
stop_listening = start_recognizer()

try:
    while True:
        time.sleep(1)  # Keep program running without blocking background thread
except KeyboardInterrupt:
    print("\nStopping Stark assistant...")
    stop_listening(wait_for_stop=False)  # Stop listening cleanly
