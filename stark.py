import pyttsx3  # Text-to-speech
import speech_recognition as sr  # Speech recognition
import time  # Time management
from openpyxl import load_workbook  # Excel handling
import random  # Random responses

# Initialize recognizer
r = sr.Recognizer()
keywords = [
    ("stark", 1), ("hey stark", 1), ("hello", 1), ("hi", 1), ("hey", 1), ("get ready", 1)
]  # Wake words
source = sr.Microphone()

print("Active Keywords:", [kw[0] for kw in keywords])

def speak(text):
    """Converts text to speech"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)  # Adjust speech speed
    engine.say(text)
    engine.runAndWait()

def callback(recognizer, audio):
    """Handles keyword detection and response"""
    try:
        speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords)
        print("Detected: ", speech_as_text)
        if any(kw in speech_as_text for kw in [kw[0] for kw in keywords]):
            speak("Yes sir?")
            recognize_main()
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")

def start_recognizer():
    """Starts keyword recognition in the background"""
    print("Waiting for a keyword...", [kw[0] for kw in keywords])
    r.listen_in_background(source, callback)
    time.sleep(1000000)  # Keeps listening indefinitely

def recognize_main():
    """Handles user commands and responses"""
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        data = r.recognize_google(audio).lower()
        print("You said:", data)
        
        if data in hello_list:
            speak(random.choice(reply_hello_list))
        elif data in how_are_you_list:
            speak(random.choice(reply_how_are_you_list))
        else:
            speak("I'm sorry sir, I did not understand your request.")
    except sr.UnknownValueError:
        print("Stark did not understand your request.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

def excel():
    """Loads predefined commands and replies from an Excel file"""
    wb = load_workbook("input.xlsx")
    wu = wb["User"]  # sets the sheet in Excel for user prompts
    wr = wb["Replies"]  # sets the sheet in Excel for replies

    global hello_list, how_are_you_list, reply_hello_list, reply_how_are_you_list
    
    urow1 = wu['1']  # hello
    urow2 = wu['2']  # how are you
    hello_list = [urow1[x].value for x in range(len(urow1))]
    how_are_you_list = [urow2[x].value for x in range(len(urow2))]

    rrow1 = wr['1']  # how are you
    rrow2 = wr['2']  # how are you
    reply_hello_list = [rrow1[x].value for x in range(len(rrow1))]
    reply_how_are_you_list = [rrow2[x].value for x in range(len(rrow2))]

# Load responses from Excel
excel()

# Start assistant
while True:
    start_recognizer()
