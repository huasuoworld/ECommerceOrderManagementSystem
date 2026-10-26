from fastapi import Depends

from ..Services.ProductsOrderService import ProductsOrderService
from ..Services.ProductsOrderPaymentService import ProductsOrderPaymentService
from .APIGatewayDefine import app, getCurrentUser
from ..Models.UsersModel import UsersModel
from ..Models.FrontEndReponseModel import ErrorResponseException

productsOrderService = ProductsOrderService()
productsOrderPaymentService = ProductsOrderPaymentService()

@app.get("/order")
async def getOrder(user: UsersModel = Depends(getCurrentUser)):
    try:
        return productsOrderService.getOrderByUserId(user.id)
    except ValueError as error:
        raise ErrorResponseException(status=400, message=str(error)) from error

@app.get("/order/confirm")
async def confirmOrder(user: UsersModel = Depends(getCurrentUser)):
    try:
        return productsOrderService.confirmOrderByUserShoppingCart(user.id)
    except ValueError as error:
        raise ErrorResponseException(status=400, message=str(error)) from error

@app.get("/order/payment")
async def orderPayment(orderId: str, user: UsersModel = Depends(getCurrentUser)):
    try:
        return productsOrderPaymentService.orderPayment(orderId, user.id)
    except ValueError as error:
        raise ErrorResponseException(status=400, message=str(error)) from error