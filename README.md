# Live Speech Conversion API 🎙️

A real-time app that turns typed text into spoken audio, streamed live over a WebSocket connection.

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)

---

## What it does

You connect to the server over a WebSocket, send it some text, and it speaks it back to you — almost instantly, with no page reload or separate file download. Under the hood, it converts your text to an audio clip and streams that audio straight back to your browser over the same live connection.

It's built to run as a small, always-on backend service (there's a `Procfile` included, so it's ready to deploy on a platform like Render or Heroku).

## How it works, in plain terms

1. Your browser opens a **WebSocket** connection to the server — a persistent, two-way channel (unlike a normal web request, it stays open so both sides can send messages anytime).
2. You send a message saying "convert this text to speech."
3. The server uses **gTTS** (Google Text-to-Speech) to generate an audio clip of that text being spoken.
4. That audio gets sent straight back over the same connection and can be played immediately in the browser.

The server can also receive audio from you — right now it just acknowledges that it got it, since actual speech-to-text (turning your voice into text) is left to the browser's own built-in speech recognition rather than being done on the server.

## Tech Stack

- **Backend:** FastAPI + WebSockets (Python)
- **Text-to-Speech:** gTTS (Google Text-to-Speech)
- **Server:** Uvicorn (ASGI server)
- **Deployment:** Configured for Render/Heroku-style platforms via `Procfile`

## Running it locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open `http://localhost:8000` in your browser.
