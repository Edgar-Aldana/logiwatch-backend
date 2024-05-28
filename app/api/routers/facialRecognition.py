from fastapi import APIRouter, WebSocket
import cv2
import numpy as np
import asyncio

facial_recognition_router = APIRouter(prefix="/facialRecognition")


def detect_color_eyes(frame):

    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Usa el clasificador de rostros de OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
    
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            eye = roi_color[ey:ey + eh, ex:ex + ew]
            eye_hsv = cv2.cvtColor(eye, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(eye_hsv, np.array([0, 50, 50]), np.array([10, 255, 255]))
            color_eye_detected = cv2.countNonZero(mask) > 0
            if color_eye_detected:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)
    
    return frame



class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: bytes):
        for connection in self.active_connections:
            await connection.send_bytes(message)

manager = ConnectionManager()



@facial_recognition_router.websocket("/websocket")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    cap = cv2.VideoCapture(0)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = detect_color_eyes(frame)
            _, buffer = cv2.imencode('.jpg', frame)
            await websocket.send_bytes(buffer.tobytes())
            await asyncio.sleep(0.03)
    except Exception as e:
        print(f"Connection closed: {e}")
    finally:
        cap.release()
