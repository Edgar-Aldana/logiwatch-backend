from pydantic import BaseModel


class accessTokenData(BaseModel):

    access_token: str | None
    type: str


class accessTokenResponse(BaseModel):

    success: bool
    detail: str
    payload: accessTokenData | None