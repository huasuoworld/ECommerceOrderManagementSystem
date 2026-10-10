from ..Models.UsersModel import UsersModel
from ..Models.FrontEndReponseModel import SuccessResponseModel, ErrorResponseModel, FileResponseModel
from ..Services.UserLoginService import UserLoginService
from ..CommonUtils import StaticFilesPath, LoggingUtil
from .APIGatewayDefine import app

# Initialize logger
user_login_service = UserLoginService()

# Define the login web page endpoint
@app.get("/", include_in_schema=False)
@app.get("/login", include_in_schema=False)
async def users_login_page():
    return FileResponseModel(path=StaticFilesPath.STATIC_WEB_DIR / "UsersLogin.html")

# Define the login endpoint
@app.post("/users/login")
async def login(userModel: UsersModel):
    LoggingUtil.logger.info("Login request received")
    sessionId = user_login_service.login(userModel)
    # TODO add cookie and session management for authenticated users
    # Here you can implement your login logic, e.g., check the username and password against a database
    if sessionId == None:
        return ErrorResponseModel()
    else:
        return SuccessResponseModel(data = sessionId)