from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from ..CommonUtils.ConstantUtil import UserSessionID, PermissionErrorCode
from ..CommonUtils.LoggingUtil import logger
from ..Models.UsersModel import UsersModel
from ..CommonUtils.ConstantUtil import STATIC_WEB_DIR, PathWhiteList, StaticPath
from ..RedisCache.RedisConnect import getSessionCache

app = FastAPI(title="My API", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_WEB_DIR), name="static")

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


@app.get("/productsOrder", include_in_schema=False)
@app.get("/my-orders", include_in_schema=False)
async def products_order_page():
    return FileResponse(STATIC_WEB_DIR / "ProductsOrder.html")


@app.middleware("http")
async def permissionCheck(request: Request, call_next):
    userSessionID = request.cookies.get(UserSessionID)
    requestPath = request.url.path
    if requestPath in PathWhiteList or requestPath.startswith(StaticPath):
        return await call_next(request)

    if not userSessionID:
        logger.info("Unauthenticated request redirected to login: %s", requestPath)
        return RedirectResponse("/login", status_code=PermissionErrorCode)

    return await call_next(request)


def getCurrentUser(request: Request) -> UsersModel:
    sessionId = request.cookies.get(UserSessionID)
    user = getSessionCache(sessionId) if sessionId else None
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user
