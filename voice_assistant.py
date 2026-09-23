# -*- coding: utf-8 -*-
import os
import re
import time
import traceback
import webbrowser

import speech_recognition as sr
import pyautogui
import pyttsx3


# ============================================================
#   RONI VOICE ASSISTANT  (English Only)
#   Version : 3.0
#   Speech  : Google Speech Recognition (en-US)
#   Feature : Say "open <anything>" -> opens that website
# ============================================================


# ============================================================
#   TEXT TO SPEECH ENGINE
# ============================================================

try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)
except Exception as e:
    print(f"[WARNING] TTS initialization error: {e}")
    engine = None


def speak(text):
    """Convert text to speech and print it to console."""
    print(f"Agent: {text}")

    if engine is None:
        return

    try:
        engine.say(text)
        engine.runAndWait()
        engine.stop()  # helps prevent the "only speaks once" bug on some systems
    except Exception as e:
        print(f"[WARNING] Voice output error: {e}")


# ============================================================
#   SPEECH RECOGNIZER
# ============================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold         = 300
recognizer.dynamic_energy_threshold = True
recognizer.dynamic_energy_adjustment_damping = 0.15
recognizer.dynamic_energy_ratio     = 1.5
recognizer.pause_threshold          = 1.0
recognizer.phrase_threshold         = 0.3
recognizer.non_speaking_duration    = 0.5


# ============================================================
#   MICROPHONE CALIBRATION
# ============================================================

def calibrate_microphone():
    """Calibrate microphone for ambient noise. Returns True on success."""
    print("\n" + "=" * 60)
    print("MICROPHONE CALIBRATION")
    print("=" * 60)
    print("Please stay quiet for 2 seconds...")
    print("Calibrating microphone...")

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=3)

        # Give it a bit of headroom above the measured ambient noise,
        # but keep it inside a sane, usable range.
        recognizer.energy_threshold = max(recognizer.energy_threshold, 50)
        if recognizer.energy_threshold > 1200:
            recognizer.energy_threshold = 600
        elif recognizer.energy_threshold < 80:
            recognizer.energy_threshold = 150

        print("Microphone calibrated successfully.")
        print(f"Energy threshold: {recognizer.energy_threshold:.0f}")
        return True

    except OSError as e:
        print("\n[ERROR] MICROPHONE ERROR")
        print(e)
        print("\nPossible solutions:")
        print("1. Check your microphone connection.")
        print("2. Check microphone permission in system settings.")
        print("3. Check default sound input device.")
        return False

    except Exception as e:
        print(f"\n[ERROR] Calibration error: {e}")
        return False


# ============================================================
#   LISTEN TO USER  (English only)
# ============================================================

def listen_command():
    """Listen to the microphone and return the recognized command as text."""
    try:
        with sr.Microphone() as source:
            print("\n" + "-" * 60)
            print("Listening... SPEAK NOW!")
            print("-" * 60)

            try:
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("No speech detected.")
                return ""

        print("Processing speech...")

        try:
            command = recognizer.recognize_google(audio, language="en-US")
            command = command.lower().strip()
            print(f"You said: {command}")
            return command

        except sr.UnknownValueError:
            print("Speech was not clear. Please speak louder and clearly.")
            # Save the captured clip so you can play it back and check
            # if the mic is actually recording your voice properly.
            try:
                with open("last_failed_audio.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                print("Saved the unclear audio as last_failed_audio.wav for review.")
            except Exception:
                pass
            return ""

        except sr.RequestError as e:
            print("\n[ERROR] Google Speech Recognition error.")
            print(e)
            print("Please check your internet connection.")
            return ""

    except OSError as e:
        print("\n[ERROR] MICROPHONE ERROR")
        print(e)
        return ""

    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        return ""


# ============================================================
#   DYNAMIC SITE OPENER
# ============================================================

# Shortcuts for common sites -> exact URL (add more anytime)
KNOWN_SITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "facebook": "https://www.facebook.com",
    "gmail": "https://mail.google.com",
    "github": "https://www.github.com",
    "chatgpt": "https://chat.openai.com",
    "claude": "https://claude.ai",
    "linkedin": "https://www.linkedin.com",
    "twitter": "https://www.twitter.com",
    "x": "https://www.x.com",
    "instagram": "https://www.instagram.com",
    "whatsapp": "https://web.whatsapp.com",
    "kaggle": "https://www.kaggle.com",
    "amazon": "https://www.amazon.com",
    "wikipedia": "https://www.wikipedia.org",
}

# Trigger words that mean "open a website"
OPEN_TRIGGERS = ["open", "launch", "go to", "start"]


def extract_site_name(command):
    """Pull the site name out of a command like 'open facebook' or 'launch netflix website'."""
    text = command

    for trigger in OPEN_TRIGGERS:
        if text.startswith(trigger + " "):
            text = text[len(trigger):].strip()
            break

    # Remove filler words
    text = re.sub(r"\b(website|site|please|the|dot com|\.com)\b", "", text)
    text = text.strip()

    return text


def listen_command_keyboard():
    """Get a command by typing instead of speaking. Returns "" on empty input."""
    try:
        command = input("\nType your command: ").lower().strip()
        return command
    except (EOFError, KeyboardInterrupt):
        raise KeyboardInterrupt


def open_website(command):
    """Open a website based on whatever name the user said."""
    site_name = extract_site_name(command)

    if not site_name:
        speak("Please tell me the site name. For example, just say: youtube.")
        return

    # Check known shortcuts first
    if site_name in KNOWN_SITES:
        url = KNOWN_SITES[site_name]
    else:
        # Build a generic URL from whatever the user said
        cleaned = site_name.replace(" ", "")
        url = f"https://www.{cleaned}.com"

    speak(f"Opening {site_name}.")
    try:
        webbrowser.open(url)
        print(f"Opened: {url}")
    except Exception as e:
        print(f"[ERROR] Could not open site: {e}")
        speak("Sorry, I could not open that site.")


def looks_like_site_request(command):
    """True if the whole command is just a site name (with no other command word)."""
    other_command_words = [
        "notepad", "calculator", "screenshot", "screen shot",
        "capture", "help", "command", "exit", "stop", "quit", "goodbye",
    ]
    if any(word in command for word in other_command_words):
        return False

    site_name = extract_site_name(command)
    return bool(site_name)


# ============================================================
#   COMMANDS : NOTEPAD
# ============================================================

def open_notepad():
    speak("Opening Notepad.")
    try:
        os.system("start notepad")
    except Exception as e:
        print(f"[ERROR] Notepad error: {e}")


# ============================================================
#   COMMANDS : CALCULATOR
# ============================================================

def open_calculator():
    speak("Opening Calculator.")
    try:
        os.system("start calc")
    except Exception as e:
        print(f"[ERROR] Calculator error: {e}")


# ============================================================
#   COMMANDS : SCREENSHOT
# ============================================================

def take_screenshot():
    speak("Taking screenshot.")
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"

        screenshot = pyautogui.screenshot()
        screenshot.save(filename)

        print(f"Screenshot saved: {os.path.abspath(filename)}")
        speak("Screenshot saved successfully.")

    except Exception as e:
        print(f"[ERROR] Screenshot error: {e}")
        speak("Sorry, I could not take the screenshot.")


# ============================================================
#   COMMANDS : HELP
# ============================================================

def show_help():
    print("\n" + "=" * 60)
    print("AVAILABLE COMMANDS")
    print("=" * 60)
    print("<any site name>        -> Opens that website (e.g. just say 'youtube')")
    print("open <any site name>   -> Also works the same way (e.g. 'open youtube')")
    print("open notepad           -> Opens Notepad")
    print("open calculator        -> Opens Calculator")
    print("take screenshot        -> Takes a screenshot")
    print("help                   -> Shows this list")
    print("exit / stop / quit     -> Closes the assistant")
    print("=" * 60)

    speak("I can open any website you name, plus Notepad, Calculator, and take screenshots.")


# ============================================================
#   COMMAND PROCESSOR
# ============================================================

def process_command(command):
    """Process the recognized command. Returns False to exit the loop."""
    if not command:
        return True

    # --- NOTEPAD (checked before generic "open") ---
    if "notepad" in command:
        open_notepad()

    # --- CALCULATOR ---
    elif "calculator" in command:
        open_calculator()

    # --- SCREENSHOT ---
    elif "screenshot" in command or "screen shot" in command or "capture" in command:
        take_screenshot()

    # --- HELP ---
    elif "help" in command or "command" in command:
        show_help()

    # --- EXIT ---
    elif command in ("exit", "stop", "quit", "goodbye"):
        speak("Goodbye.")
        return False

    # --- DYNAMIC WEBSITE OPEN (with trigger word) ---
    elif any(command.startswith(t + " ") for t in OPEN_TRIGGERS):
        open_website(command)

    # --- DYNAMIC WEBSITE OPEN (bare name, no trigger word needed) ---
    elif looks_like_site_request(command):
        open_website(command)

    # --- UNKNOWN ---
    else:
        print(f"Unknown command: {command}")
        speak("Sorry, I don't understand that command. Try just saying a site name, like youtube.")

    return True


# ============================================================
#   MAIN AGENT
# ============================================================

def run_agent():
    print("\n" + "=" * 60)
    print("RONI VOICE ASSISTANT")
    print("=" * 60)
    print("Version: 3.1 (English Only, Voice + Keyboard)")
    print("Speech Recognition: Google")
    print("=" * 60)

    print("\nChoose input mode:")
    print("1. Voice (microphone)")
    print("2. Keyboard (type commands)")
    mode = input("Enter 1 or 2: ").strip()

    use_keyboard = (mode == "2")

    if not use_keyboard:
        microphone_ready = calibrate_microphone()
        if not microphone_ready:
            print("\n[ERROR] Assistant cannot start in voice mode.")
            print("Switching to keyboard mode instead.")
            use_keyboard = True

    speak("Voice assistant is ready. Please give your command.")

    while True:
        if use_keyboard:
            command = listen_command_keyboard()
        else:
            command = listen_command()

        if not command:
            time.sleep(0.3)
            continue

        try:
            should_continue = process_command(command)
        except Exception as e:
            print("\n[ERROR] Something went wrong while running that command:")
            traceback.print_exc()
            speak("Sorry, something went wrong with that command.")
            should_continue = True

        if not should_continue:
            break

        time.sleep(0.3)


# ============================================================
#   PROGRAM START
# ============================================================

if __name__ == "__main__":
    try:
        run_agent()

    except KeyboardInterrupt:
        print("\n\nAssistant stopped by user.")
        try:
            speak("Assistant stopped.")
        except Exception:
            pass

    except Exception as e:
        print("\n[ERROR] FATAL ERROR")
        traceback.print_exc()
