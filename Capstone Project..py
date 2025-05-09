import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import pywhatkit
import os

def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # 0 for male, 1 for female
    engine.say(audio)
    engine.runAndWait()

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.7
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print("You said:", query)
        except Exception as e:
            print("Error:", e)
            speak("Please say that again.")
            return "None"
        return query

def get_day():
    day = datetime.datetime.today().weekday() + 1
    days = {
        1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday',
        5: 'Friday', 6: 'Saturday', 7: 'Sunday'
    }
    if day in days.keys():
        speak("Today is " + days[day])

def get_time():
    now = datetime.datetime.now()
    hour = now.strftime("%H")
    minute = now.strftime("%M")
    speak(f"It is {hour} hours and {minute} minutes.")

def greet_user():
    if os.path.exists("Welcome.txt"):
        with open("Welcome.txt", "r") as f:
            speak(f.read())
    else:
        speak("Welcome back. Initializing your assistant.")
    get_day()
    get_time()

def main_query():
    greet_user()
    speak("You better have a good reason for coming here.")
    
    while True:
        query = listen_command().lower()

        if "message on whatsapp" in query:
            speak("Who is the unlucky person?")
            if os.path.exists("WhatsApp.txt"):
                with open("WhatsApp.txt", "r") as f:
                    print(f.read())
            phone_number = input("Enter the phone number (with country code, e.g., +911234567890): ")
            speak("Is there a message or are we planning on spamming someone?")
            message = input("Enter the message: ")
            hour = int(input("Enter the hour in 24-hour format: "))
            minutes = int(input("Enter the minutes: "))
            speak("Your Highness, your precious message is being delivered now.")
            pywhatkit.sendwhatmsg(phone_number, message, hour, minutes)

        elif "search something" in query:
            speak("Seeking knowledge now, are we?")
            search_query = input("Enter what you seek to find: ")
            speak("Your wish is my command.")
            webbrowser.open("https://www.google.com/search?q=" + search_query)
            break

        elif "play some music" in query:
            speak("Opening Spotify now.")
            webbrowser.open("https://open.spotify.com/playlist/6pz9V85VH4McSTf1Y9eVfg")
            break

        elif "go back to sleep" in query:
            if os.path.exists("Goodbye.txt"):
                with open("Goodbye.txt", "r") as f:
                    speak(f.read())
            else:
                speak("Goodbye. Going back to sleep.")
            break

        elif "none" in query:
            continue
        else:
            speak("I didn't quite catch that. Please try again.")

# Start the assistant
if __name__ == "__main__":
    main_query()
