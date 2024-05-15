from pydantic import BaseModel

class LoginRequest(BaseModel):

    email_address: str
    password: str    