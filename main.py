from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import io
import base64
import os
import asyncio
import wave
import tempfile

app = FastAPI(title="Live Speech Conversion API")

# Add CORS middleware for Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [KEEP ALL YOUR HTML CONTENT EXACTLY AS IS - IT'S CORRECT]

@app.get("/")
async def get():
    return HTMLResponse(html_content)


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)


manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            # Receive data from client
            data = await websocket.receive()

            if 'text' in data:
                message = data['text']
                try:
                    message_data = eval(message)

                    if message_data.get('type') == 'audio':
                        # Handle audio data - just acknowledge receipt
                        await manager.send_personal_message({
                            "type": "status",
                            "message": "Audio received. For speech-to-text, please use browser's built-in speech recognition."
                        }, websocket)

                    elif message_data.get('type') == 'text_to_speech':
                        # Handle text-to-speech (this still works)
                        text = message_data.get('text', '')

                        if text:
                            try:
                                # Convert text to speech
                                tts = gTTS(text=text, lang='en')

                                # Save to bytes buffer
                                audio_buffer = io.BytesIO()
                                tts.write_to_fp(audio_buffer)
                                audio_buffer.seek(0)

                                # Convert to base64 for sending over websocket
                                audio_base64 = base64.b64encode(audio_buffer.read()).decode('utf-8')

                                # Send audio back
                                await manager.send_personal_message({
                                    "type": "audio",
                                    "audio": audio_base64
                                }, websocket)

                            except Exception as e:
                                await manager.send_personal_message({
                                    "type": "error",
                                    "message": f"Text-to-speech error: {str(e)}"
                                }, websocket)

                except Exception as e:
                    await manager.send_personal_message({
                        "type": "error",
                        "message": f"Invalid message format: {str(e)}"
                    }, websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)

# Add this for Render deployment
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)