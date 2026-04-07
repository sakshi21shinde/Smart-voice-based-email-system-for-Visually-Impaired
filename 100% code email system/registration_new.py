import tkinter as tk
from tkinter import messagebox as ms
import sqlite3
import re
import random
import speech_recognition as sr
import time
import pyttsx3
import cv2
from translate import Translator
import os
import platform
from subprocess import call

def create_db():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        first_name TEXT,
                        last_name TEXT,
                        username TEXT,
                        user_id TEXT)''')  # Removed photo_captured and trained columns
    
    conn.commit()
    conn.close()

def insert_user(first_name, last_name, username, user_id):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (first_name, last_name, username, user_id) VALUES (?, ?, ?, ?)",
                   (first_name, last_name, username, user_id))  # Removed photo_captured and trained
    
    conn.commit()
    conn.close()

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()

def recognize_speech(prompt):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        speak(prompt)
        print(prompt)
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            print(f"Recognized: {text}")
            speak(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand. Please try again.")
            return recognize_speech(prompt)
        except sr.RequestError as e:
            speak(f"Could not request results from Google Speech Recognition; {e}")
            return None

# Create the database
create_db()

speak("Welcome to your Blind Email Registration.")

first_name = recognize_speech("Speak your First Name")
last_name = recognize_speech("Speak your Last Name")
username = recognize_speech("Please say your username")
user_id = recognize_speech("Please enter your user ID, for example, one two three")

insert_user(first_name, last_name, username, user_id)  # Removed photo_captured and trained


photo_captured = 0
trained = 0

if recognize_speech("Do you want to capture your photo? Say Yes or No").lower() in ['yes', 'yes yes', 'say yes']:
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    sampleN = 0
    
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sampleN += 1
            cv2.imwrite(f"Image/User.{user_id}.{sampleN}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.waitKey(100)
        cv2.imshow('img', img)
        cv2.waitKey(1)
        if sampleN > 40:
            break
    cap.release()
    cv2.destroyAllWindows()
    speak("Photo captured successfully")
    photo_captured = 1
    
    if recognize_speech("Do you want to train your photo? Say Yes or No").lower() in ['yes', 'yes yes', 'say yes']:
        call(["python", "train.py"])
        trained = 1
        speak("Registration successful. Welcome to the login page.")
        call(["python", "face_login.py"])
else:
    speak("Registration Unsuccessful. Please Try Again.")