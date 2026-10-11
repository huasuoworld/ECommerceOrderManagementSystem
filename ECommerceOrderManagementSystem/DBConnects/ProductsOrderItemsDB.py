from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .NewBaseDB import NewBaseDB
from ..Models.ProductsOrderItemsModel import ProductsOrderItemsModel
from typing import List
from ..CommonUtils.ConstantUtil import DBExcludeColumns, getCurrentTime
from .SQLiteDB import getDB

class ProductsOrderItemsDB(NewBaseDB):
    __tablename__ = 'products_order_items'

    products_order_id = Column(Integer)
    users_id = Column(Integer)
    products_id = Column(Integer)
    products_discount_id = Column(Integer)
    products_inventory_id = Column(Integer)
    product_name = Column(String)
    product_code = Column(String)
    item_quantity = Column(Integer)
    item_ordder_number = Column(String)
    item_product_price = Column(Integer)
    item_discount_price = Column(Integer)
    item_unit_price = Column(Integer)

    def createProductsOrderItems(
        self,
        db: Session,
        productsOrderItemsModelList: List[ProductsOrderItemsModel],
    ) -> List["ProductsOrderItemsDB"]:
        productsOrderItemsDBDataList = []
        for productsOrderItemsModel in productsOrderItemsModelList:
            productsOrderItemData: ProductsOrderItemsModel = productsOrderItemsModel.model_dump(
                exclude=DBExcludeColumns
            )
            timestamp = getCurrentTime()
            productsOrderItemData.created_at = timestamp
            productsOrderItemData.updated_at = timestamp
            productsOrderItemsDBDataList.append(ProductsOrderItemsDB(**productsOrderItemData))
        db.add_all(productsOrderItemsDBDataList)
        db.flush()
        return productsOrderItemsDBDataList