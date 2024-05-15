from datetime import datetime, timedelta
from dotenv import load_dotenv
from jose import jwt
from jose.exceptions import JWTError
from app.admin.schemas.input.loginInputSchemas import LoginRequest
from os import getenv

load_dotenv()


class token():

    SECRET_KEY = getenv("SECRET_KEY")
    ALGORITHM = getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRES_MINUTES = getenv("ACCESS_TOKEN_EXPIRES_MINUTES")

    def create(data: dict):

        SECRET_KEY = getenv("SECRET_KEY")
        ALGORITHM = getenv("ALGORITHM")
        ACCESS_TOKEN_EXPIRES_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=float(ACCESS_TOKEN_EXPIRES_MINUTES))
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

