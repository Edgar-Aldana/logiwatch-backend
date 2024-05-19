from typing import Optional
from pydantic import BaseModel

class LoginRequest(BaseModel):

    email_address: str
    password: str    



class SignupRequest(BaseModel):

    nombres: str
    apellidoPaterno: str
    apellidoMaterno: str

    correo: str
    password: str
    telefono: str

    posicion: str
    region: str
    matriculaVehiculo: Optional[str] = None

