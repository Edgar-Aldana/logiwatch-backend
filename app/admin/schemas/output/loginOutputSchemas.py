from pydantic import BaseModel
from app.admin.schemas.output.generalOutputSchemas import Response


class accessTokenData(BaseModel):

    access_token: str | None
    type: str


class accessTokenResponse(Response):

    payload: accessTokenData | None



class signupData(BaseModel):

    user: str | None



class signupResponse(Response):

    payload: signupData


