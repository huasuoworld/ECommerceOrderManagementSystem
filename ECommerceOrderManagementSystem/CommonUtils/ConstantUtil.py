from pathlib import Path
import datetime, uuid

STATIC_WEB_DIR = Path(__file__).resolve().parent.parent / "StaticsWeb"

SuccessStatusCode = 200
ErrorStatusCode = 400
PermissionErrorCode = 303
DoNotHavePermissionErrorCode = 401
ShoppingCartNoDataErrorCode = 601
InsufficientAvailableStockError = 701
InsufficientReservedStockError = 702
InsufficientInventoryStockError = 703
ProductIdIsNoneErrorCode = 801
DoNotHavePermissionErrorMessage = "Unauthenticated request"
CouldNotFindUserErrorCode = "404"
CouldNotFindUserErrorMessage = "Could not find the user's profile"
ShoppingCartNoDataErrorMessage = "There's no data in the shipping cart"
InsufficientAvailableStockMessage = "Insufficient available stock"
InsufficientReservedStockMessage = "Insufficient reserved stock"
InsufficientInventoryStockMessage = "Insufficient inventory stock"
ProductIdIsNoneErrorMessage = "Product id is null"

StaticPath = "/static/"

SuccessMessage = "Success"
ErrorMessage = "Error"

UserSessionID = "userSessionID"

PathWhiteList = ["/", "/login", "/users/login", "/docs", "/openapi.json"]
BuyerPathWhiteList = ["/products", "/products/listProducts", "/order", "/order/confirm", "/order/payment", "/shoppingCart", "/shoppingCart/items", "/shoppingCart/items", "/users/me"]
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
PaymentPrefix = "PAY-"

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

DBExcludeColumnsWithoutId = {"page_number", "page_size", "seller_id"}
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

def getPaymentNumber():
    return PaymentPrefix + str(uuid.uuid4())