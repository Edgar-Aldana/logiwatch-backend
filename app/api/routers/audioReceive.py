# from fastapi import APIRouter, Form
# from fastapi.responses import JSONResponse
# import os
# from gtts import gTTS
# from playsound import playsound
# import uuid

# from app.api.schemas.messageReceiveInputSchemas import TextReceive

# audio_receive_router = APIRouter(prefix="/audioCommunication")

# AUDIO_DIR = './audio_files'
# os.makedirs(AUDIO_DIR, exist_ok=True)

# @audio_receive_router.post("/receiveText")
# async def receive_text(request: TextReceive):
#     try:
#         unique_filename = f"received_audio_{uuid.uuid4()}.mp3"
#         audio_file_path = os.path.join(AUDIO_DIR, unique_filename)
        
#         # Convierte el texto a audio usando gTTS
#         tts = gTTS(text=request.message, lang='es')
#         tts.save(audio_file_path)

#         # Reproduce el archivo
#         playsound(audio_file_path)

#         return JSONResponse(content={"message": "Text received and played successfully"}, status_code=200)
#     except Exception as e:
#         print(e)
#         return JSONResponse(content={"message": f"Error processing text to audio: {e}"}, status_code=500)


from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os
from gtts import gTTS
import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.api.schemas.messageReceiveInputSchemas import TextReceive

audio_receive_router = APIRouter(prefix="/audioCommunication")

AUDIO_DIR = './audio_files'
os.makedirs(AUDIO_DIR, exist_ok=True)

# Executor para manejar la reproducción de audio en un hilo separado
executor = ThreadPoolExecutor(max_workers=1)

def play_audio(file_path):
    from playsound import playsound
    playsound(file_path)

@audio_receive_router.post("/receiveText")
async def receive_text(request: TextReceive):
    try:
        unique_filename = f"received_audio_{uuid.uuid4()}.mp3"
        audio_file_path = os.path.join(AUDIO_DIR, unique_filename)
        
        # Convierte el texto a audio usando gTTS
        tts = gTTS(text=request.message, lang='es')
        tts.save(audio_file_path)

        # Reproduce el archivo en un hilo separado para no bloquear el evento
        loop = asyncio.get_event_loop()
        loop.run_in_executor(executor, play_audio, audio_file_path)

        return JSONResponse(content={"message": "Text received and played successfully"}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": f"Error processing text to audio: {e}"}, status_code=500)