from pathlib import Path

STATIC_WEB_DIR = Path(__file__).resolve().parent.parent / "StaticsWeb"

SuccessStatusCode = 200
ErrorStatusCode = 400
PermissionErrorCode = 303

StaticPath = "/static/"

SuccessMessage = "Success"
ErrorMessage = "Error"

UserSessionID = "userSessionID"

PathWhiteList = ["/", "/login"]