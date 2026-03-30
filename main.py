import asyncio
import edge_tts
import pygame
import time
import os
import webbrowser
import ollama
import requests
import speech_recognition as sr
from datetime import datetime


reminders = []

pygame.mixer.init()
is_speaking = False

r = sr.Recognizer()
r.energy_threshold = 300
r.pause_threshold = 0.8


async def speak(text):
    global is_speaking
    is_speaking = True

    filename = "voice.mp3"

    communicate = edge_tts.Communicate(
        text,
        "en-IN-NeerjaNeural"
    )

    await communicate.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)

    pygame.mixer.music.unload()
    try:
        os.remove(filename)
    except:
        pass

    is_speaking = False


async def listen():
    global is_speaking

    if is_speaking:
        return ""

    loop = asyncio.get_running_loop()

    def _listen_blocking():
        with sr.Microphone() as source:
            print("🎤 Listening...")
            r.adjust_for_ambient_noise(source, duration=0.5)

            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            except:
                return ""

        try:
            text = r.recognize_google(audio)
            print("You:", text)
            return text.lower()
        except:
            return ""

    return await loop.run_in_executor(None, _listen_blocking)


async def quick_commands(text):
    now = datetime.now()

    if "date" in text or "aaj date kya hai" in text:
        date = now.strftime("%d %B %Y")
        await speak(f"Aaj ki date {date} hai")
        return True

    if "time" in text or "samay" in text:
        current_time = now.strftime("%I:%M %p")
        await speak(f"Abhi time {current_time} hai")
        return True

    if "day" in text or "aaj ka din" in text:
        day = now.strftime("%A")
        await speak(f"Aaj {day} hai")
        return True

    if "youtube" in text:
        webbrowser.open("https://www.youtube.com")
        await speak("YouTube khol raha hoon")
        return True

    if "open chrome" in text:
        os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        await speak("Chrome khol raha hoon")
        return True

    if "open edge" in text:
        os.startfile(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
        await speak("Edge khol raha hoon")
        return True

    if "open calculator" in text:
        os.startfile("calc.exe")
        await speak("Calculator khol raha hoon")
        return True

    if "open notepad" in text:
        os.startfile("notepad.exe")
        await speak("Notepad khol raha hoon")
        return True

    if "reminder" in text:
        await set_reminder(text)
        return True

    if "news" in text:
        await get_news()
        return True

    if "score" in text or "match" in text:
        await get_score()
        return True

    return False


def extract_reminder_topic(text):
    prompt = f"Extract only the core reminder topic from this sentence: '{text}'. Reply ONLY with the topic."
    try:
        response = ollama.chat(
            model="llama3:8b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content'].strip()
    except:
        return text


def ask_ai(text):
    try:
        response = ollama.chat(
            model="llama3:8b",
            messages=[
                {
                    "role": "system",
                    "content": "Your name is Jarvis. You are an AI Voice Assistant. You are a helpful assistant that speaks in short Hinglish and sounds natural."
                },
                {"role": "user", "content": text}
            ]
        )
        return response['message']['content'].strip()
    except:
        return "Bhai kuch error aa gaya"


async def process(text):
    if await quick_commands(text):
        return

    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(None, ask_ai, text)

    print("Jarvis:", response)

    if any(word in text for word in [
        "search", "find", "documentation", "doc", "tutorial", "guide"
    ]):
        webbrowser.open(f"https://www.google.com/search?q={text}")
        await speak("Searching kar raha hoon")
    else:
        await speak(response)


async def set_reminder(text):
    try:
        words = text.split()
        minutes = 1

        for word in words:
            if word.isdigit():
                minutes = int(word)

        loop = asyncio.get_running_loop()
        message = await loop.run_in_executor(None, extract_reminder_topic, text)

        async def reminder_task():
            await asyncio.sleep(minutes * 60)
            await speak(f"Reminder: {message}")

        asyncio.create_task(reminder_task())

        await speak(f"Reminder set for {minutes} minute")

    except:
        await speak("Reminder set nahi ho paya")


async def get_news():
    try:
        url = "https://newsapi.org/v2/top-headlines?language=en&apiKey=8c5354cf2dd44abe83c22442461b826c"
        headers = {"User-Agent": "Mozilla/5.0"}

        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, lambda: requests.get(url, headers=headers))
        data = response.json()

        articles = data.get("articles", [])

        if not articles:
            await speak("Koi news available nahi hai")
            return

        await speak("Top headlines suno")

        for i, article in enumerate(articles[:3]):
            await speak(article.get("title", ""))

    except:
        await speak("News fetch nahi ho payi")


async def get_score():
    await speak("Live score ke liye Google open kar raha hoon")
    webbrowser.open("https://www.google.com/search?q=live cricket score")


async def main():
    print("🚀 Jarvis started...")
    await speak("Hello bhai, main Jarvis hoon")

    while True:
        text = await listen()

        if not text:
            await asyncio.sleep(0.1)
            continue

        if "exit" in text or "bye" in text:
            await speak("Goodbye bhai")
            break

        await process(text)


if __name__ == "__main__":
    asyncio.run(main())