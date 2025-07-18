import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import difflib
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext

# === Text-to-Speech Engine Setup ===
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# === Command List with Aliases ===
commands = {
    "open google": ["open google", "launch google", "go to google", "google kholo", "start google"],
    "open youtube": ["open youtube", "launch youtube", "start youtube", "youtube kholo", "play youtube"],
    "open notepad": ["open notepad", "start notepad", "notepad kholo", "launch notepad"],
    "shutdown": ["shutdown", "turn off computer", "shut down", "band kar do", "power off"],
    "exit": ["exit", "close program", "band ho ja", "quit", "close assistant"],
    "open chrome": ["open chrome", "launch chrome", "chrome kholo", "start chrome"],
    "open whatsapp": ["open whatsapp", "whatsapp kholo", "launch whatsapp"],
    "open calculator": ["open calculator", "calculator kholo", "start calculator"],
    "open command prompt": ["open cmd", "launch cmd", "command prompt kholo"],
    "open control panel": ["open control panel", "control panel kholo"],
    "open task manager": ["open task manager", "task manager kholo"],
    "play music": ["play music", "music chalao", "start music", "gaana bajao"],
    "pause music": ["pause music", "music band karo"],
    "search google": ["search google", "google par search karo", "do a google search", "search something"],
    "lock screen": ["lock screen", "screen lock karo", "lock the pc"],
    "open settings": ["open settings", "settings kholo", "launch settings"],
    "take screenshot": ["take screenshot", "screen capture", "screenshot le lo"],
    "open paint": ["open paint", "paint kholo", "launch paint"],
    "open explorer": ["open explorer", "explorer kholo", "file explorer"],
    "restart pc": ["restart pc", "reboot system", "restart computer", "system restart"],
}

def find_best_match(user_input):
    all_phrases = []
    phrase_to_command = {}

    for cmd, phrases in commands.items():
        for phrase in phrases:
            all_phrases.append(phrase)
            phrase_to_command[phrase] = cmd

    best_match = difflib.get_close_matches(user_input.lower(), all_phrases, n=1, cutoff=0.6)
    if best_match:
        return phrase_to_command[best_match[0]]
    return None

# === Handle Recognized Commands ===
def handle_commands(command):
    matched_command = find_best_match(command)
    
    if matched_command == "open google":
        webbrowser.open("https://www.google.com")
        speak("Opening Google 🌐")
    elif matched_command == "open youtube":
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube 🎬")
    elif matched_command == "open notepad":
        os.system("notepad")
        speak("Opening Notepad 📝")
    elif matched_command == "shutdown":
        speak("Shutting down... 💻")
        os.system("shutdown /s /t 1")
    elif matched_command == "exit":
        speak("Goodbye! 👋")
        window.quit()
    elif matched_command == "open chrome":
        os.system("start chrome")
        speak("Opening Chrome 🌍")
    elif matched_command == "open whatsapp":
        webbrowser.open("https://web.whatsapp.com")
        speak("Opening WhatsApp 💬")
    elif matched_command == "open calculator":
        os.system("calc")
        speak("Opening Calculator 🧮")
    elif matched_command == "open command prompt":
        os.system("start cmd")
        speak("Opening Command Prompt 🖥️")
    elif matched_command == "open control panel":
        os.system("control")
        speak("Opening Control Panel ⚙️")
    elif matched_command == "open task manager":
        os.system("taskmgr")
        speak("Opening Task Manager 📊")
    elif matched_command == "play music":
        speak("Playing music 🎵")
        os.system("start wmplayer")  # Default player
    elif matched_command == "pause music":
        speak("Pause command received 🛑 (manual pause needed)")
    elif matched_command == "search google":
        speak("What should I search?")
        command = recognize_text()
        webbrowser.open(f"https://www.google.com/search?q={command}")
    elif matched_command == "lock screen":
        os.system("rundll32.exe user32.dll,LockWorkStation")
        speak("Locking screen 🔒")
    elif matched_command == "open settings":
        os.system("start ms-settings:")
        speak("Opening Settings ⚙️")
    elif matched_command == "take screenshot":
        speak("Press Win + PrtSc to take screenshot 📸")
    elif matched_command == "open paint":
        os.system("mspaint")
        speak("Opening Paint 🎨")
    elif matched_command == "open explorer":
        os.system("explorer")
        speak("Opening File Explorer 📂")
    elif matched_command == "restart pc":
        speak("Restarting your PC 🔁")
        os.system("shutdown /r /t 1")
    else:
        speak("Sorry, I couldn't understand. 😕")
        output_box.insert(tk.END, "❗ Unrecognized command\n")

# === Recognize Text ===
def recognize_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="🎙️ Listening...")
        window.update()
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5)
            status_label.config(text="🔎 Recognizing...")
            window.update()
            text = recognizer.recognize_google(audio, language='en-IN')
            output_box.insert(tk.END, f"🗣️ You said: {text}\n")
            save_to_file(text)
            return text
        except:
            output_box.insert(tk.END, "❗ Couldn't understand audio\n")
            return ""

# === Main Function for Button ===
def recognize_and_handle():
    user_text = recognize_text()
    if user_text:
        handle_commands(user_text)

# === Save Recognized Text ===
def save_to_file(text):
    with open("recognized_text.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]: {text}\n")

# === GUI Setup ===
window = tk.Tk()
window.title("🧠 Smart Voice Assistant")
window.geometry("700x500")
window.configure(bg="#f0f0f0")

title_label = tk.Label(window, text="🎤 Smart Voice Assistant", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)

start_button = tk.Button(window, text="▶ Start Listening", command=recognize_and_handle,
                         font=("Arial", 14), bg="#007BFF", fg="white", padx=20, pady=10)
start_button.pack(pady=10)

output_box = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=15, font=("Consolas", 12), bg="white")
output_box.pack(pady=10)

status_label = tk.Label(window, text="Click 'Start Listening' and speak...", font=("Arial", 12), bg="#f0f0f0", fg="green")
status_label.pack()

window.mainloop()
