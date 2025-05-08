import pyttsx3  # Text-to-speech
import speech_recognition as sr  # Speech recognition
import time  # Time management
import subprocess  # To open/close applications
import os  # System operations
import pyautogui  # Keyboard shortcuts for volume control
from ctypes import cast, POINTER  # For precise volume control
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from openpyxl import load_workbook  # Excel handling
import random  # Random responses
import datetime  # Date and time functionalities
import requests  # For weather API
from openai_integration import ask_openai 
from dotenv import load_dotenv
# Initialize recognizer
r = sr.Recognizer()
keywords = [("stark", 1), ("hey stark", 1), ("hello", 1), ("hi", 1), ("hey", 1), ("get ready", 1)]
source = sr.Microphone()

print("Active Keywords:", [kw[0] for kw in keywords])
load_dotenv()
# Text-to-Speech Function
def speak(text):
    """Converts text to speech"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)  # Adjust speech speed
    engine.say(text)
    engine.runAndWait()

# Control System Volume
def set_volume(level):
    """Sets system volume to a specific level (0-100)"""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    volume.SetMasterVolumeLevelScalar(level / 100, None)
    speak(f"Volume set to {level} percent.")

def volume_control(action):
    """Controls volume (up, down, mute) using pyautogui"""
    if action == "up":
        pyautogui.press("volumeup")
        speak("Volume increased.")
    elif action == "down":
        pyautogui.press("volumedown")
        speak("Volume decreased.")
    elif action == "mute":
        pyautogui.press("volumemute")
        speak("Volume muted.")

# Open Applications
def open_app(app_name):
    """Opens applications based on predefined mappings"""
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "command prompt": "cmd.exe",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
    }

    if app_name in apps:
        subprocess.Popen(apps[app_name])
        speak(f"Opening {app_name}.")
    else:
        speak(f"Sorry, I don't know how to open {app_name} yet.")

# Weather Report Function
API_KEY = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
def get_weather(city):
    """Fetches weather details for the given city"""
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        speak(f"The current temperature in {city} is {temp}°C with {description}.")
    else:
        speak("Sorry, I couldn't fetch the weather details. Please try again.")

# Close Applications
def close_app(app_name):
    """Closes applications using taskkill"""
    app_processes = {
        "notepad": "notepad.exe",
        "calculator": "CalculatorApp.exe",
        "chrome": "chrome.exe",
        "command prompt": "cmd.exe",
        "word": "WINWORD.EXE"
    }

    if app_name in app_processes:
        os.system(f"taskkill /F /IM {app_processes[app_name]}")
        speak(f"Closing {app_name}.")
    else:
        speak(f"I couldn't find {app_name} running.")

# Recognize Speech Commands
def recognize_main():
    """Handles user commands and responses"""
    with sr.Microphone() as source:
        print("Say something!")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5)
            data = r.recognize_google(audio).lower()
            print("You said:", data)

            if "weather in" in data:
                city = data.split("weather in")[-1].strip()
                get_weather(city)
            elif data in hello_list:
                hour = datetime.datetime.now().hour
                if hour < 12:
                    speak("Good morning, sir")
                elif hour < 18:
                    speak("Good afternoon, sir")
                else:
                    speak("Good evening, sir")
            elif "what is the time" in data:
                current_time = datetime.datetime.now().strftime("%H:%M")
                speak(f"The time is {current_time}")
            elif "what day is it" in data:
                day_of_week = datetime.datetime.today().strftime("%A")
                speak(f"Today is {day_of_week}")
            elif "open" in data:
                app_name = data.replace("open", "").strip()
                open_app(app_name)
            elif "close" in data:
                app_name = data.replace("close", "").strip()
                close_app(app_name)
            elif "volume up" in data:
                volume_control("up")
            elif "volume down" in data:
                volume_control("down")
            elif "mute volume" in data:
                volume_control("mute")
            elif "set volume to" in data:
                try:
                    level = int(data.split()[-1])
                    if 0 <= level <= 100:
                        set_volume(level)
                    else:
                        speak("Volume level must be between 0 and 100.")
                except ValueError:
                    speak("Please specify a valid volume level.")
            else:
                # Send unrecognized input to OpenAI
                response = ask_openai(data)
                speak(response)
        except sr.UnknownValueError:
            print("Stark did not understand your request.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except sr.WaitTimeoutError:
            print("Listening timed out.")

# Load Excel Data
def load_excel_data():
    """Loads predefined commands and replies from an Excel file"""
    try:
        wb = load_workbook("input.xlsx", data_only=True)
        wu, wr = wb["User"], wb["Replies"]

        global hello_list, how_are_you_list, reply_hello_list, reply_how_are_you_list
        
        hello_list = [cell.value for cell in wu[1] if cell.value]  # Avoid empty values
        how_are_you_list = [cell.value for cell in wu[2] if cell.value]
        reply_hello_list = [cell.value for cell in wr[1] if cell.value]
        reply_how_are_you_list = [cell.value for cell in wr[2] if cell.value]

        print("Excel data loaded successfully.")
    except Exception as e:
        print(f"Error loading Excel file: {e}")

# Keyword Activation
def callback(recognizer, audio):
    """Handles keyword detection and response"""
    try:
        speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=keywords)
        print("Detected:", speech_as_text)
        if any(kw[0] in speech_as_text.split() for kw in keywords):
            speak("Yes sir?")
            recognize_main()
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")

def start_recognizer():
    """Starts keyword recognition in the background"""
    print("Waiting for a keyword...", [kw[0] for kw in keywords])
    r.listen_in_background(source, callback)
    time.sleep(1000000)  # Keeps listening indefinitely

# Load responses from Excel
load_excel_data()

# Start Assistant
while True:
    start_recognizer()
