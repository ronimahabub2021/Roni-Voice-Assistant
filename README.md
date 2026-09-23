# 🎙️ Roni Voice Assistant

**Roni Voice Assistant** is a lightweight Windows-based voice assistant built with Python. It can listen to English voice commands, recognize speech using Google Speech Recognition, open websites, launch Windows applications, take screenshots, and respond using text-to-speech.

The project is designed as a simple foundation for building a more advanced personal AI assistant.

## ✨ Features

* 🎤 English voice command recognition
* 🗣️ Text-to-speech responses
* 🌐 Open websites using voice commands
* 📝 Open Windows Notepad
* 🧮 Open Windows Calculator
* 📸 Take screenshots
* ⌨️ Keyboard command mode
* 🎚️ Automatic microphone calibration
* 🔊 Ambient-noise adjustment
* 💾 Saves unclear audio for microphone debugging
* 🛑 Voice commands for stopping the assistant
* 🧩 Easy to extend with new commands

## 🛠️ Technologies

* **Python 3**
* **SpeechRecognition** — Speech-to-text
* **Google Speech Recognition** — English speech recognition
* **PyAudio** — Microphone input
* **pyttsx3** — Text-to-speech
* **PyAutoGUI** — Screenshot capture
* **Webbrowser** — Website launching

## 📁 Project Structure

```text
Roni-Voice-Assistant/
│
├── roni_voice_assistant.py
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
```

## ⚙️ Requirements

### Software

* Windows 10/11
* Python 3.10+
* Git
* Working microphone
* Internet connection for Google Speech Recognition

### Python Packages

Install the required packages with:

```bash
pip install -r requirements.txt
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/ronimahabub2021/Roni-Voice-Assistant.git
```

### 2. Enter the project directory

```bash
cd Roni-Voice-Assistant
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, you can use:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the assistant

```bash
python roni_voice_assistant.py
```

## 🎤 Usage

When the program starts, you can choose:

```text
1. Voice (microphone)
2. Keyboard (type commands)
```

### Voice Mode

Select:

```text
1
```

The assistant will calibrate your microphone and then wait for commands.

Example commands:

```text
youtube
```

```text
open youtube
```

```text
open google
```

```text
open github
```

```text
open notepad
```

```text
open calculator
```

```text
take screenshot
```

```text
help
```

```text
exit
```

## 🌐 Supported Websites

Some commonly supported websites include:

* YouTube
* Google
* Facebook
* Gmail
* GitHub
* ChatGPT
* Claude
* LinkedIn
* X / Twitter
* Instagram
* WhatsApp Web
* Kaggle
* Amazon
* Wikipedia

The project also supports dynamically opening websites by name.

For example:

```text
open netflix
```

## ⌨️ Keyboard Mode

If the microphone is unavailable, select:

```text
2
```

You can then type commands manually.

Example:

```text
open youtube
```

or:

```text
take screenshot
```

## 🎙️ Microphone Calibration

Before voice recognition starts, Roni Voice Assistant performs automatic ambient-noise calibration.

The program measures background noise and adjusts the microphone energy threshold accordingly.

This helps improve speech detection in different environments.

## 🔧 Troubleshooting

### Microphone is not detected

Check:

1. Microphone connection
2. Windows microphone permissions
3. Default Windows input device
4. Python/PyAudio installation

Test PyAudio:

```bash
python -c "import pyaudio; print('PyAudio OK')"
```

### Speech is not recognized

Try:

* Speaking closer to the microphone
* Speaking clearly
* Reducing background noise
* Checking your internet connection
* Using keyboard mode

The assistant may save unclear audio as:

```text
last_failed_audio.wav
```

This file can be used for debugging microphone input.

## 🔐 Privacy

This project uses Google Speech Recognition through the `SpeechRecognition` library for voice-to-text processing.

Voice commands may therefore be sent to Google's speech recognition service for processing.

Do not use the application with sensitive or confidential audio if you do not want that audio processed by a third-party service.

## 🚧 Future Improvements

Planned improvements include:

* 🤖 Local LLM integration
* 🧠 AI-powered natural language command processing
* 💬 ChatGPT/API integration
* 🦙 Ollama local model support
* 🇧🇩 Bangla voice recognition
* 🌍 Multi-language support
* 📂 File and folder management
* 📧 Email automation
* 🔎 Web search
* 📝 Notes and reminders
* 📅 Calendar integration
* 💻 Advanced Windows automation
* 🎵 Media control
* 🔐 User authentication
* 🧠 Long-term memory
* 🗣️ Wake-word detection
* ⚡ Offline speech recognition with Whisper

## 🧑‍💻 Author

**Md. Roni Mahabub**

AI Engineer | Machine Learning | Data Science | Python

GitHub:
https://github.com/ronimahabub2021

## 📄 License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this project according to the terms of the license.

---

⭐ If you find this project useful, consider giving it a star on GitHub!
