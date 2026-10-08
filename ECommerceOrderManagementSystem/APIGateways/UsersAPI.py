import logging
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from ..Services.UserLoginService import UserLoginService

logger = logging.getLogger(__name__)
STATIC_WEB_DIR = Path(__file__).resolve().parent.parent / "StaticsWeb"

app = FastAPI(title="My API", version="1.0.0")
app.mount("/static", StaticFiles(directory=STATIC_WEB_DIR), name="static")
user_login_service = UserLoginService()


@app.get("/", include_in_schema=False)
@app.get("/login", include_in_schema=False)
async def users_login_page():
    return FileResponse(STATIC_WEB_DIR / "UsersLogin.html")


class UsersAPI(BaseModel):
    username: str
    password: str


@app.post("/users/login")
async def login(user: UsersAPI):
    logger.info("Login request received")
    is_authenticated = user_login_service.login(user.username, user.password)
    # Here you can implement your login logic, e.g., check the username and password against a database
    if is_authenticated:
        return {"message": "Login successful"}
    else:
        return {"message": "Invalid username or password"}