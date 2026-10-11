from __future__ import annotations

from typing import Optional

from .ProductsModel import ProductsModel
from .ProductsInventoryModel import ProductsInventoryModel
from .ProductsDiscountModel import ProductsDiscountModel

#extend from products model
class ProductsDiscountInventoryModel(ProductsModel):
    #products_discount model
    products_discount_id: Optional[int] = None
    discount_price: Optional[int] = None
    discount_person_limit_stock: Optional[int] = None
    discount_stock: Optional[int] = None
    #products_inventory model
    products_inventory_id: Optional[int] = None
    warehouse_name: Optional[str] = None
    inventory_stock: Optional[int] = None
    inventory_available_stock: Optional[int] = None
    inventory_status: Optional[str] = None
    

    class Config:
                from_attributes = True

    #copy productsInventory to productsDiscountInventory
    @staticmethod
    def copyProductsInventoryToThisModel(productsInventory: ProductsInventoryModel, productsDiscountInventory: ProductsDiscountInventoryModel):
        if productsDiscountInventory == None:
            productsDiscountInventory = ProductsDiscountInventoryModel()
        if productsInventory == None:
            return productsDiscountInventory
        productsDiscountInventory.products_inventory_id = productsInventory.id
        productsDiscountInventory.inventory_stock = productsInventory.inventory_stock
        productsDiscountInventory.warehouse_name = productsInventory.warehouse_name
        productsDiscountInventory.inventory_available_stock = productsInventory.inventory_available_stock
        productsDiscountInventory.inventory_status = productsInventory.inventory_status
        productsDiscountInventory.seller_id = productsInventory.seller_id
        return productsDiscountInventory

    #copy productsDiscount to productsDiscountInventory
    @staticmethod
    def copyProductsDiscountToThisModel(productsDiscount: ProductsDiscountModel, productsDiscountInventory: ProductsDiscountInventoryModel):
        if productsDiscountInventory == None:
            productsDiscountInventory = ProductsDiscountInventoryModel()
        if productsDiscount == None:
            return productsDiscountInventory
        productsDiscountInventory.products_discount_id = productsDiscount.id
        productsDiscountInventory.discount_person_limit_stock = productsDiscount.discount_person_limit_stock
        productsDiscountInventory.discount_price = productsDiscount.discount_price
        productsDiscountInventory.discount_stock = productsDiscount.discount_stock
        productsDiscountInventory.seller_id = productsDiscount.seller_id
        return productsDiscountInventory