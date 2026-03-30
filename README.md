# 🎙️ Jarvis: Personal AI Voice Assistant

Jarvis is an intelligent, asynchronous voice assistant built with Python. It leverages the power of **Ollama (Llama 3)** for natural language processing and **Microsoft Edge TTS** for highly realistic voice synthesis. Designed for speed and reliability.

---

## ✨ Key Features

* **Advanced Conversational AI:** Integrated with `Llama 3:8b` via Ollama for sophisticated and context-aware responses.
* **Asynchronous Engine:** Built on `asyncio`, allowing the assistant to process tasks and manage reminders in the background without freezing the UI.
* **Realistic TTS:** Utilizes `edge-tts` (Neerja Neural) for high-quality, human-like voice output.
* **System Automation:** * **App Control:** Quick launch for Chrome, Edge, Calculator, and Notepad.
    * **Web Integration:** Automated YouTube navigation and Google search capabilities.
* **Smart Utilities:**
    * **Dynamic Reminders:** Set time-based reminders using natural language.
    * **Live Updates:** Fetches top news headlines via NewsAPI and live cricket scores.
    * **Temporal Awareness:** Instant reporting of current date, day, and time.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **LLM Engine** | Ollama (Llama 3) |
| **Speech-to-Text** | SpeechRecognition (Google API) |
| **Text-to-Speech** | Edge-TTS (Microsoft) |
| **Audio Engine** | Pygame Mixer |
| **Web Services** | NewsAPI, Webbrowser, Requests |

---

## 🚀 Installation & Setup

1. Ensure **Ollama** is running with `llama3`.
2. Install dependencies:
   ```bash
   pip install asyncio edge-tts pygame ollama requests speechrecognition
   ```
## 🏃 How to Run
   To start the assistant, navigate to your project directory and run:

   ```bash
   python main.py
   ```
   Note: Ensure your microphone is connected and the Ollama service is running in the background.
