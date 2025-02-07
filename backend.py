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

# 🔄 Carrega o modelo uma única vez
model = None  

def get_model():
    """Carrega o modelo Whisper apenas uma vez para evitar recarregamento em cada requisição."""
    global model
    if model is None:
        print("🚀 Carregando o modelo Whisper pela primeira vez...")
        model = whisper.load_model("tiny")  # Mantém o modelo na memória
    return model

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    audio_path = file_path.rsplit(".", 1)[0] + ".mp3"

    # 🔊 Extrai áudio do vídeo
    audio = AudioSegment.from_file(file_path)
    audio.export(audio_path, format="mp3")

    # 🎤 Obtém o modelo Whisper carregado na memória
    model = get_model()
    
    print("⚡️ Iniciando transcrição...")
    result = model.transcribe(audio_path)
    
    print("✅ Transcrição concluída!")
    return {"transcription": result["text"]}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8080))  
    # ⏳ Aumenta tempo de keep-alive para evitar timeout no Railway
    uvicorn.run(app, host="0.0.0.0", port=port, timeout_keep_alive=120)
