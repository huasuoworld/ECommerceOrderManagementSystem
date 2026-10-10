from fastapi import Depends, HTTPException, Request
from pydantic import BaseModel, Field

from ..Services.ShoppingCartService import ShoppingCartService
from .APIGatewayDefine import app
from ..CommonUtils.ConstantUtil import UserSessionID
from ..RedisCache.RedisConnect import getSessionCache
from ..Models.UsersModel import UsersModel

shoppingCartService = ShoppingCartService()


class AddCartItemRequest(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(default=1, gt=0)


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(gt=0)


def getCurrentUser(request: Request) -> UsersModel:
    sessionId = request.cookies.get(UserSessionID)
    user = getSessionCache(sessionId) if sessionId else None
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


@app.get("/shoppingCart")
async def getShoppingCart(user: UsersModel = Depends(getCurrentUser)):
    return shoppingCartService.getCart(user.id)


@app.post("/shoppingCart/items")
async def addShoppingCartItem(
    request: AddCartItemRequest,
    user: UsersModel = Depends(getCurrentUser),
):
    try:
        return shoppingCartService.addItem(user.id, request.product_id, request.quantity)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Product not found") from error


@app.patch("/shoppingCart/items/{product_id}")
async def updateShoppingCartItem(
    product_id: int,
    request: UpdateCartItemRequest,
    user: UsersModel = Depends(getCurrentUser),
):
    try:
        return shoppingCartService.updateQuantity(user.id, product_id, request.quantity)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Cart item not found") from error


@app.delete("/shoppingCart/items/{product_id}")
async def removeShoppingCartItem(
    product_id: int,
    user: UsersModel = Depends(getCurrentUser),
):
    try:
        return shoppingCartService.removeItem(user.id, product_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Cart item not found") from error