import datetime
import webbrowser
import os
import playsound
import time
import threading
import speech_recognition as d
import gtts
import wikipedia
import subprocess
import re
import requests as r
import json
import pyttsx3
import wolframalpha
import tkinter

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

rate = engine.getProperty('rate')
engine.setProperty('rate', 150)


def say(text):
    try:
        tts = gtts.gTTS(text=text, lang="en-us")
        date = datetime.datetime.now()
        file_name = str(str(date).replace(":", "-") +
                        "-voice.mp3").replace(' ', '')
        tts.save(file_name)
        print("Olivia: " + text)
        playsound.playsound(file_name)
        os.remove(file_name)
    except:
        engine.say(text)
        engine.runAndWait()
        print("Olivia: " + text)


def wishUser():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        say("Hi, Good Morning")
    elif hour >= 12 and hour < 18:
        say("Hi, Good Afternoon")
    else:
        say("Hi, Good Evening")
    say("I am Olivia. How can I help?")


def get_audio():
    r = d.Recognizer()
    with d.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print("You: " + said)
        except Exception as e:
            if e != "":
                print("Error:", e)
    return said.lower()


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)
    subprocess.Popen(["notepad.exe", file_name])


def google():
    url = "https://www.google.co.in/search?q="
    say("What do you want to search?")
    search_text = get_audio().lower()
    say("Opening google...")
    webbrowser.open(url+search_text)


def replies(text):
    if "search" in text:
        if text == "search":
            google()
        else:
            se = text.replace("search ", "")
            say("Opening google...")
            webbrowser.open("https://www.google.co.in/search?q=" + str(se))
    elif "thank" in text:
        say("It's my pleasure to work for you!")
        quit()
    elif "give me information about" in text:
        try:
            wiki = text.replace("give me information about ", "")
            s = wikipedia.summary(wiki, sentences=2)
            say("According to wikipedia, " + str(s))
        except:
            pass
    elif "bye" in text:
        say("Nice to meet you")
        quit()
    elif text == "":
        pass
    elif "what" in text:
        if "time" in text:
            now = str(datetime.datetime.now().strftime("%H:%M:%S"))
            say("The time is " + now)
        elif "is" in text:
            try:
                wiki = text.replace("what is ", "")
                s = wikipedia.summary(wiki, sentences=2)
                say("According to wikipedia, " + str(s))
            except:
                pass
        elif "are" in text:
            try:
                wiki = text.replace("what are ", "")
                s = wikipedia.summary(wiki, sentences=2)
                say("According to wikipedia, " + str(s))
            except:
                pass
    elif "who is" in text:
        try:
            wiki = text.replace("who is ", "")
            s = wikipedia.summary(wiki, sentences=2)
            say("According to wikipedia, " + str(s))
        except:
            pass
    elif 'ask something' in text:
        say('What do you want to ask?')
        question = get_audio()
        client = wolframalpha.Client(wolfram_API)
        res = client.query(question)
        answer = next(res.results).text
        say(answer)
    else:
        say("I don't understand")
        say("You want to google it?")
        yn_text = get_audio()
        if "yes" in yn_text:
            url = "https://www.google.co.in/search?q="
            say("Opening google...")
            webbrowser.open(url+text)


def run():
    wishUser()
    WAKE = "hey olivia"
    while True:
        print("Listening")
        text = get_audio()

        if text.count(WAKE) > 0:
            say("Hey there, try saying 'make a note' or 'search'")
            text = get_audio()

        NOTE_STRS = ["make a note", "remember this"]

        for phrase in NOTE_STRS:
            if phrase in text:
                say("what would you like me to write down?")
                note_text = get_audio()
                note_text = note_text.replace("next line ", "\n")
                note_text = note_text.replace("full stop", ".")
                note_text = note_text.replace("slash", "/")
                note(note_text)
                say("I've made a note of that")
                run()

        replies(text)


run()
