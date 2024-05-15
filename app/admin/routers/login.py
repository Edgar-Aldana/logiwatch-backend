from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from app.admin.models.users import Monitoristas
from app.admin.schemas.input.loginInputSchemas import LoginRequest
from app.admin.services.login_services import AuthService

auth_router = APIRouter(prefix='/auth')


@auth_router.post("/login")
async def get_access_token(request: LoginRequest):

    response = AuthService.ValidateRegisteredUser(request)
    return JSONResponse(status_code=200, content=response.dict())