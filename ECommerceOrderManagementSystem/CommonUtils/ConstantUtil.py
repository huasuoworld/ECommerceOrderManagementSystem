from pathlib import Path
import datetime, uuid

STATIC_WEB_DIR = Path(__file__).resolve().parent.parent / "StaticsWeb"

SuccessStatusCode = 200
ErrorStatusCode = 400
PermissionErrorCode = 303
DoNotHavePermissionErrorCode = 401
DoNotHavePermissionErrorMessage = "Unauthenticated request"
CouldNotFindUserErrorCode = "404"
CouldNotFindUserErrorMessage = "Could not find the user's profile"

StaticPath = "/static/"

SuccessMessage = "Success"
ErrorMessage = "Error"

UserSessionID = "userSessionID"

PathWhiteList = ["/", "/login", "/users/login"]
BuyerPathWhiteList = ["/products", "/products/listProducts", "/order", "/order/confirm", "/shoppingCart", "/shoppingCart/items", "/shoppingCart/items", "/users/me"]
AdminPathWhiteList = BuyerPathWhiteList + ["/management/users/listUsers", "/usersManagement", "/management/users/active", "/management/users/inactive"]
SellerPathWhiteList = BuyerPathWhiteList + ["/products/listProductsBySellerId", "/productsManagement", "/products/listProductsBySellerId", "/productsOrder"]

AdminHomePageURL = "/usersManagement"
SellerHomePageURL = "/productsManagement"
BuyerHomePageURL = "/products"
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

UserStatusActive = "active"
UserStatusInactive = "inactive"

PermissionStatusActive = "active"
PermissionStatusInactive = "inactive"

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