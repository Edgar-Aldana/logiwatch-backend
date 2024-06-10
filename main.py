from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

#Models and Engines
import app.admin.models as AdminModels
from app.database_connection import engine


#Routers
from app.admin.routers import login
from app.api.routers import facialRecognition
from app.api.routers import audioReceive

app = FastAPI()


# try create all models
try:
    AdminModels.Base.metadata.create_all(bind=engine, checkfirst=True)
    print("The models were created correctly")
except Exception as error:
    print(error)
    print("No models to load")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



#Routers
app.include_router(login.auth_router)
app.include_router(facialRecognition.facial_recognition_router)
app.include_router(audioReceive.audio_receive_router)





@app.get("/")
async def home():

    responseData = {"success": True, "message": "Welcome", "payload": None}
    return JSONResponse(status_code=200, content=responseData)

    
