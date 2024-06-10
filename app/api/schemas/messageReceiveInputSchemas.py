from pydantic import BaseModel

class TextReceive(BaseModel):

    message: str
