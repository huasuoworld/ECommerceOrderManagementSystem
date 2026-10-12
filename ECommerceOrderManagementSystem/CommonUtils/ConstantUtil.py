from pathlib import Path
import datetime, uuid

STATIC_WEB_DIR = Path(__file__).resolve().parent.parent / "StaticsWeb"

SuccessStatusCode = 200
ErrorStatusCode = 400
PermissionErrorCode = 303

StaticPath = "/static/"

SuccessMessage = "Success"
ErrorMessage = "Error"

UserSessionID = "userSessionID"

PathWhiteList = ["/", "/login", "/users/login"]
AdminPathWhiteList = ["/management/users/listUsers", "/usersManagement"]
SellerPathWhiteList = ["/products/listProductsBySellerId", "/productsManagement"]
UsersManagementURL = "/usersManagement"
ProductsManagementURL = "/productsManagement"
AdminPermission = "/admin"
SellerPermission = "/seller"
BuyerPermission = "/buyer"
HttpUrl = "http_url"
SessionId = "sessionId"

OrderPrefix = "ORD-"

PaymentStatusUnpaid = "Unpaid"
PaymentStatusPaying = "Paying"
PaymentStatusPaid = "Paid"
PaymentStatusFailed = "Failed"

OrderStatusUnpaid = "Unpaid"
OrderStatusPaid = "Paid"
OrderStatusShipped = "Shipped"
OrderStatusCompleted = "Completed"
OrderStatusCancelled = "Cancelled"
OrderStatusRefunded = "Refunded"

DBExcludeColumns = {"id", "page_number", "page_size"}
DBExcludeShoppingCartColumns = DBExcludeColumns | {
    "users_id",
    "unit_price",
    "products_total_price",
}

def getCurrentTime():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getUUID4():
    return uuid.uuid4()

def getOrderNumber():
    return OrderPrefix + str(uuid.uuid4())