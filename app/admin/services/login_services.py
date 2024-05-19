from app.admin.schemas.output.loginOutputSchemas import accessTokenData, accessTokenResponse
from app.utils.decode import token
from ..schemas.input.loginInputSchemas import LoginRequest, SignupRequest
from app.admin.models.users import Empleados



class AuthService():

    user: str
    token: str
    algorithm: str


    def GetAccessToken(user):

        if not len(user):
            return None
        
        return token.create({"user": user[0].correo})
        

    
    def ValidateRegisteredUser(request: LoginRequest):

        user = Empleados.find(correo=request.email_address, password=request.password)
        accessToken = AuthService.GetAccessToken(user)
        tokenData: accessTokenData = accessTokenData(access_token=accessToken, type="Bearer")

        if not accessToken:
            accessTokenPayload: accessTokenResponse = accessTokenResponse(success=False, detail="User not found !!", payload=None)
        else:
            accessTokenPayload: accessTokenResponse = accessTokenResponse(success=True, detail="access token !!!", payload=tokenData)

        return accessTokenPayload


    def createUser(userData: SignupRequest):

        userExists = Empleados.find(correo=userData.correo)
        if not len(userExists):
            return Empleados.create(**userData.dict())
        else:
            return None