import cv2
import mediapipe as mp
import base64
import json
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
from mediapipe.python.solutions.drawing_utils import DrawingSpec

# Inicializar enrutador de API
facial_recognition_router = APIRouter(prefix="/facialRecognition")

# Clase para manejar conexiones WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.capture_started = False

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        if not self.capture_started:
            asyncio.create_task(self.video_capture())
            self.capture_started = True

    def disconnect(self, websocket: WebSocket):
        try:
            self.active_connections.remove(websocket)
        except:
            pass
        if not self.active_connections:
            self.capture_started = False

    async def broadcast(self, message):
        for connection in self.active_connections:
            try:
                await connection.send_bytes(message) 
            except WebSocketDisconnect:
                self.disconnect(connection)
            except Exception as e:
                print(f"Error broadcasting: {e}")

    async def video_capture(self):
        cap = cv2.VideoCapture(0)
        frame_rate = 20  # Tasa de frames por segundo
        frame_interval = 1.0 / frame_rate  # Intervalo entre frames
        
        # Inicializar MediaPipe Face Detection
        mp_face_detection = mp.solutions.face_detection
        mp_drawing = mp.solutions.drawing_utils
        face_detection = mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5)
        

        try:
            while self.active_connections:
                start_time = asyncio.get_event_loop().time()
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)  # Voltear horizontalmente
                
                # Convertir el frame a RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Procesar el frame con MediaPipe Face Detection
                results = face_detection.process(frame_rgb)

                # Dibujar las detecciones de rostros en el frame
                if results.detections:
            
                    for detection in results.detections:
                        mp_drawing.draw_detection(frame, detection, DrawingSpec(color=(0,255,0)))
                        nose_tip = mp_face_detection.get_key_point(
                            detection, mp_face_detection.FaceKeyPoint.NOSE_TIP)
                        if nose_tip.y > 0.5:  # Se inclina hacia abajo
                            mp_drawing.draw_detection(frame, detection, DrawingSpec(color=(0,255,255)))
                            message = {"type": "alert", "data": {"alert": "SOMNOLIENTO"}}
                            json_message = json.dumps(message)
                            asyncio.create_task(self.broadcast(json_message))

                # Codificar el frame como JPEG con calidad óptima
                #encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]
                _, buffer = cv2.imencode('.jpg', frame)

                # Enviar los datos binarios del frame a través de la conexión WebSocket
                encoded_data = base64.b64encode(buffer.tobytes()).decode('utf-8')
                message = {"type": "frame", "data": encoded_data}
                json_message = json.dumps(message)
                await self.broadcast(json_message)
                
                # Controlar la tasa de frames
                elapsed_time = asyncio.get_event_loop().time() - start_time
                await asyncio.sleep(max(0, frame_interval - elapsed_time))
        finally:
            cap.release()
            face_detection.close()

manager = ConnectionManager()

# Endpoint WebSocket para transmitir la captura de video
@facial_recognition_router.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Connection error: {e}")


