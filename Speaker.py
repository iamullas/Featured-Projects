import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty("rate", 150)  # Speed of speech
engine.setProperty("volume", 1.0)  # Volume level

# Speak text
engine.say("Hello! This is a Python script talking to you.")
engine.runAndWait()
