from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import whisper
import shutil
import os
from pydub import AudioSegment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

model = whisper.load_model("tiny")

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    audio_path = file_path.rsplit(".", 1)[0] + ".mp3"

    # Extrair áudio do vídeo
    audio = AudioSegment.from_file(file_path)
    audio.export(audio_path, format="mp3")

    # Transcrição usando Whisper
    result = model.transcribe(audio_path)

    return {"transcription": result["text"]}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8080))  
    uvicorn.run(app, host="0.0.0.0", port=port)
