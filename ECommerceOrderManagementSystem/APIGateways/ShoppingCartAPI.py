from fastapi import HTTPException
from pydantic import BaseModel, Field

from ..Services.ShoppingCartService import ShoppingCartService
from .APIGatewayDefine import app

shopping_cart_service = ShoppingCartService()


class AddCartItemRequest(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(default=1, gt=0)


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(gt=0)


@app.get("/shoppingCart")
async def getShoppingCart():
    return shopping_cart_service.getCart()


@app.post("/shoppingCart/items")
async def addShoppingCartItem(request: AddCartItemRequest):
    try:
        return shopping_cart_service.addItem(request.product_id, request.quantity)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Product not found") from error


@app.patch("/shoppingCart/items/{product_id}")
async def updateShoppingCartItem(product_id: int, request: UpdateCartItemRequest):
    try:
        return shopping_cart_service.updateQuantity(product_id, request.quantity)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Cart item not found") from error


@app.delete("/shoppingCart/items/{product_id}")
async def removeShoppingCartItem(product_id: int):
    try:
        return shopping_cart_service.removeItem(product_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Cart item not found") from error