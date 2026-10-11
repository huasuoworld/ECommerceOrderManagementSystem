from fastapi import Depends, HTTPException

from ..Services.ProductsOrderService import ProductsOrderService
from .APIGatewayDefine import app, getCurrentUser
from ..Models.UsersModel import UsersModel

productsOrderService = ProductsOrderService()

@app.get("/order")
async def getOrder(user: UsersModel = Depends(getCurrentUser)):
    return productsOrderService.getOrderByUserId(user.id)

@app.get("/order/confirm")
async def confirmOrder(user: UsersModel = Depends(getCurrentUser)):
    try:
        return productsOrderService.confirmOrderByUserShoppingCart(user.id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error