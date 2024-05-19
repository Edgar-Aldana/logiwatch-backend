from typing import Union
from pydantic import BaseModel


class Response(BaseModel):

    success: bool
    detail: str
    payload: Union[str, int, None]


