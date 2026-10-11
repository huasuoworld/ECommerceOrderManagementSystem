from __future__ import annotations

from .UsersBaseModel import UsersBaseModel
from typing import List
from .FrontEndReponseModel import PageDataReponseModel
from .ProductsModel import ProductsModel

#ProductsInventory model
class ProductsInventoryModel(UsersBaseModel):
    product_id: int
    warehouse_name: str
    warehouse_code: str
    inventory_stock: int
    inventory_reserved_stock: int
    inventory_available_stock: int
    inventory_status: str

    class Config:
            from_attributes = True

    def getProductsInventoryIDList(productsInventoryPageList: PageDataReponseModel):
        if productsInventoryPageList.items == None:
            return None
        productsInventoryList = productsInventoryPageList.items
        return [productsInventory.id for productsInventory in productsInventoryList]

    def getPageInfo(productsModel: ProductsModel, productsInventoryModel: ProductsInventoryModel):
        productsInventoryModel.page_size = productsModel.page_size
        productsInventoryModel.page_number = productsModel.page_number
        return productsInventoryModel