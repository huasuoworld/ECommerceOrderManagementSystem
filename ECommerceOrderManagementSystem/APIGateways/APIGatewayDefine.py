from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from ..CommonUtils.ConstantUtil import UserSessionID, PermissionErrorCode
from ..CommonUtils.LoggingUtil import logger

from ..CommonUtils.ConstantUtil import STATIC_WEB_DIR, PathWhiteList, StaticPath

app = FastAPI(title="My API", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_WEB_DIR), name="static")


@app.get("/products", include_in_schema=False)
async def products_page():
    return FileResponse(STATIC_WEB_DIR / "Products.html")

@app.middleware("http")
async def permissionCheck(request: Request, call_next):
    userSessionID = request.cookies.get(UserSessionID)
    isAuthenticated = True
    requestPath = request.url.path
    #check url is in the white list
    if(requestPath in PathWhiteList or requestPath.startswith(StaticPath)):
        isAuthenticated = True
        return await call_next(request)
    else:
        #TODO check user permission
        logger.info("userSessionID: ", userSessionID)
        #check userSessionID, if not redirect to the login page
        if not isAuthenticated:
            return RedirectResponse("/login", status_code = PermissionErrorCode)
