import tkinter as tk
from tkinter import messagebox
import threading
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime

engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_and_transcribe():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        update_status("🎙️ Listening... Please speak.")
        try:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=None)
            update_status("⏹️ Transcribing...")
            command = recognizer.recognize_google(audio)
            update_output(f"You said: {command}")
            handle_command(command.lower())
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            update_output("Didn't catch that.")
        except sr.RequestError:
            speak("API unavailable.")
            update_output("Speech API error.")
        update_status("🎤 Click to Listen")

def handle_command(cmd):
    if "time" in cmd:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")
        update_output(f"The time is {now}")
    elif "open youtube" in cmd:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "open google" in cmd:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "exit" in cmd or "quit" in cmd:
        speak("Goodbye!")
        root.quit()
    else:
        speak("I don't know that one yet.")
        update_output("Command not recognized.")

def start_listening():
    threading.Thread(target=listen_and_transcribe).start()

def update_status(text):
    status_label.config(text=text)

def update_output(text):
    output_text.config(state='normal')
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, text)
    output_text.config(state='disabled')

def copy_transcript():
    text = output_text.get("1.0", tk.END).strip()
    root.clipboard_clear()
    root.clipboard_append(text)
    messagebox.showinfo("Copied", "Transcript copied to clipboard.")

# GUI setup
root = tk.Tk()
root.title("Smart Voice Assistant")
root.geometry("500x420")
root.resizable(False, False)
root.configure(bg="#1e1e2f")

FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_BUTTON = ("Segoe UI", 14)
FONT_TEXT = ("Segoe UI", 12)

title_label = tk.Label(root, text="🧠 Smart Voice Assistant", font=FONT_TITLE, bg="#1e1e2f", fg="#ffffff")
title_label.pack(pady=10)

status_label = tk.Label(root, text="🎤 Click to Listen", font=FONT_TEXT, bg="#1e1e2f", fg="#bbbbbb")
status_label.pack(pady=5)

speak_button = tk.Button(root, text="🎙️ Listen & Transcribe", command=start_listening,
                         font=FONT_BUTTON, bg="#2e2e3f", fg="white", padx=10, pady=5)
speak_button.pack(pady=10)

output_frame = tk.Frame(root, bg="#1e1e2f")
output_frame.pack(pady=5, fill=tk.BOTH, expand=True)

output_text = tk.Text(output_frame, height=6, font=FONT_TEXT, wrap="word", bg="#2e2e3f", fg="white", bd=0)
output_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
output_text.config(state='disabled')

copy_button = tk.Button(root, text="📋 Copy Transcript", command=copy_transcript,
                        font=FONT_TEXT, bg="#3a3a4f", fg="white")
copy_button.pack(pady=5)

footer = tk.Label(root, text="Jagrat Sharma • 2024", font=("Segoe UI", 9), bg="#1e1e2f", fg="#666666")
footer.pack(side=tk.BOTTOM, pady=5)

root.mainloop()