from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from app.admin.models.users import Empleados
from app.admin.schemas.input.loginInputSchemas import LoginRequest, SignupRequest
from app.admin.schemas.output.loginOutputSchemas import signupData, signupResponse
from app.admin.services.login_services import AuthService

auth_router = APIRouter(prefix='/auth')


@auth_router.post("/login")
async def get_access_token(request: LoginRequest):

    response = AuthService.ValidateRegisteredUser(request)
    return JSONResponse(status_code=200, content=response.dict())



@auth_router.post("/signup")
async def signup(request: SignupRequest):

    newUser = AuthService.createUser(request)
    statusCode = 201
    success = True
    detail = "user created !!!"

    if not newUser:
        statusCode = 202
        success = False
        detail = "user exists in database, no created !!!"
        userData: signupData = signupData(user=newUser)
    else:
        userData: signupData = signupData(user=newUser.correo)

    response: signupResponse = signupResponse(success=success, detail=detail, payload=userData).dict()
    return JSONResponse(status_code=statusCode, content=response)




