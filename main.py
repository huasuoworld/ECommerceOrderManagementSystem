import importlib
import sys
from pathlib import Path

import uvicorn

PROJECT_DIR = Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

database_package = importlib.import_module("ECommerceOrderManagementSystem.DBConnects")
sys.modules["DBConnects"] = database_package

for module_name in ("UsersDB", "UsersPermissionRulesDB"):
    qualified_name = f"ECommerceOrderManagementSystem.DBConnects.{module_name}"
    sys.modules[f"DBConnects.{module_name}"] = importlib.import_module(qualified_name)

app = importlib.import_module(
    "ECommerceOrderManagementSystem.APIGateways.Application"
).app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
