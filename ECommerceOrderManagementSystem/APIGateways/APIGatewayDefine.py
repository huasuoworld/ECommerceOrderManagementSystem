import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from ..CommonUtils.ConstantUtil import UserSessionID, PermissionErrorCode
from ..CommonUtils.LoggingUtil import logger
from ..Models.UsersModel import UsersModel
from ..Models.UsersPermissionRulesModel import UsersPermissionRulesModel
from ..CommonUtils.ConstantUtil import STATIC_WEB_DIR, PathWhiteList, StaticPath, AdminPathWhiteList, SellerPathWhiteList, AdminPermission, SellerPermission, DoNotHavePermissionErrorCode, DoNotHavePermissionErrorMessage
from ..RedisCache.RedisConnect import getSessionCache
from ..Services.PermissionValidationService import PermissionValidationService
from ..Models.FrontEndReponseModel import ErrorResponseModel, ErrorResponseException
from ..CommonUtils.LoggingUtil import logger

permissionValidationService = PermissionValidationService()

app = FastAPI(title="My API", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_WEB_DIR), name="static")


def errorResponse(error: ErrorResponseException) -> JSONResponse:
    body = ErrorResponseModel(
        status = error.status,
        message = error.message,
        error_code = error.error_code,
        details = error.details,
    ).model_dump()
    return JSONResponse(status_code = error.status, content = body)


@app.exception_handler(ErrorResponseException)
async def handleErrorResponse(request: Request, error: ErrorResponseException) -> JSONResponse:
    return errorResponse(error)


# Define the login web page endpoint
@app.get("/", include_in_schema=False)
@app.get("/login", include_in_schema=False)
async def users_login_page():
    return FileResponse(STATIC_WEB_DIR / "UsersLogin.html")

@app.get("/products", include_in_schema=False)
async def products_page():
    return FileResponse(STATIC_WEB_DIR / "Products.html")


@app.get("/productsManagement", include_in_schema=False)
async def products_management_page():
    return FileResponse(STATIC_WEB_DIR / "ProductsManagement.html")


@app.get("/usersManagement", include_in_schema=False)
async def users_management_page():
    return FileResponse(STATIC_WEB_DIR / "UsersManagement.html")


@app.get("/productsOrder", include_in_schema=False)
@app.get("/my-orders", include_in_schema=False)
async def products_order_page():
    return FileResponse(STATIC_WEB_DIR / "ProductsOrder.html")


@app.middleware("http")
async def permissionCheck(request: Request, call_next):
    try:
        userSessionID = request.cookies.get(UserSessionID)
        requestPath = request.url.path
        if requestPath in PathWhiteList or requestPath.startswith(StaticPath):
            return await call_next(request)

        if not userSessionID:
            logger.info("Unauthenticated request redirected to login: %s", requestPath)
            return RedirectResponse("/login", status_code=PermissionErrorCode)
    
        user = getCurrentUser(request)
        hasPermission: bool = True

        permissionValidationList = permissionValidationService.getUserPermission(user.id)
        #if hasPermission then pass then throw exception
        hasPermission = permissionValidationService.hasPermissionByList(requestPath, permissionValidationList)
        logger.info("Unauthenticated request, hasPermission: %s", hasPermission)
        if hasPermission:
            return await call_next(request)

        raise ErrorResponseException(status = DoNotHavePermissionErrorCode, message = DoNotHavePermissionErrorMessage)
    except ErrorResponseException as error:
        return errorResponse(error)

def getCurrentUser(request: Request) -> UsersModel:
    sessionId = request.cookies.get(UserSessionID)
    user = getSessionCache(sessionId) if sessionId else None
    if user is None:
        raise ErrorResponseException(status = DoNotHavePermissionErrorCode, message = DoNotHavePermissionErrorMessage)
    return user

if __name__ == "__main__":
  uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)