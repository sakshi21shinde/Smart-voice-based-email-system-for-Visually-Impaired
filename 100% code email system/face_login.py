import tkinter as tk
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
import re
import random
import speech_recognition as sr
import time
from translate import Translator
import os
import cv2
import subprocess
import pyttsx3  # System Text-to-Speech

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Set voice speed
engine.setProperty("volume", 1.0)  # Max volume

def speak(text):
    """ Function to play system audio without saving as MP3 """
    engine.say(text)
    engine.runAndWait()

# Load face recognition model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainingdata.yml')
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
font = cv2.FONT_HERSHEY_SIMPLEX

# Open camera
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # Set width
cam.set(4, 480)  # Set height

minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

def authenticate_user():
    """ Authenticate user and proceed if speech is recognized as 'ok' """
    speak('Authenticated User... Login successfully... Welcome to the Email System.')

    r = sr.Recognizer()
    print("Please say 'ok' to continue...")
    speak("Please say 'ok' to continue...")

    with sr.Microphone() as source:
        try:
            audio_data = r.record(source, duration=5)
            print("Recognizing speech...")
            text = r.recognize_google(audio_data).lower()
            print(f"Recognized text: {text}")

            if text == 'ok':
                speak("Proceeding to open your emails.")
                result = subprocess.run(["python", "email_system.py"], capture_output=True, text=True)
                print(result.stdout)
                if result.stderr:
                    print("Error:", result.stderr)
            else:
                speak("Invalid response. Exiting.")
        except sr.UnknownValueError:
            speak("Sorry, I could not understand your speech.")
        except sr.RequestError as e:
            speak(f"Speech recognition service error: {e}")

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 8, minSize=(int(minW), int(minH)))

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        if confidence < 60:
            confidence_text = f"  {100 - confidence:.0f}%"
            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, confidence_text, (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

            cam.release()
            cv2.destroyAllWindows()
            authenticate_user()
            break
        else:
            id = "Unknown Person Identified"
            confidence_text = f"  {100 - confidence:.0f}%"
            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, confidence_text, (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

            cam.release()
            cv2.destroyAllWindows()
            speak('Unauthenticated User... Closing...')
            print('Oops! Unauthenticated User detected.')
            break

    cv2.imshow('camera', img)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
