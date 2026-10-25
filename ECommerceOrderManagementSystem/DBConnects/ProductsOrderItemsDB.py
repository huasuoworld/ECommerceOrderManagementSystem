import json
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from ..CommonUtils.LoggingUtil import logger
from .UsersBaseDB import UsersBaseDB
from ..Models.ProductsOrderItemsModel import ProductsOrderItemsModel
from typing import List
from ..CommonUtils.ConstantUtil import DBExcludeColumnsWithoutId, getCurrentTime
from .SQLiteDB import getDB

class ProductsOrderItemsDB(UsersBaseDB):
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

    def createProductsOrderItems(self, db: Session, productsOrderItemsModelList: List[ProductsOrderItemsModel],
    ) -> List["ProductsOrderItemsDB"]:
        productsOrderItemsDBDataList = []
        timestamp = getCurrentTime()
        for productsOrderItemsModel in productsOrderItemsModelList:
            productsOrderItemData = productsOrderItemsModel.model_dump(exclude = DBExcludeColumnsWithoutId)
            productsOrderItem = ProductsOrderItemsDB(**productsOrderItemData)
            productsOrderItem.created_at = timestamp
            productsOrderItem.updated_at = timestamp
            productsOrderItemsDBDataList.append(productsOrderItem)
            logger.info("productsOrderItem %s", productsOrderItemData)    
        db.add_all(productsOrderItemsDBDataList)
        db.flush()
        return productsOrderItemsDBDataList

    #get order items
    def getProductsOrderItems(self, productOrderId: int):
        with getDB() as db:
            if productOrderId is None:
                    return None
            orderItems = db.query(ProductsOrderItemsDB).filter(ProductsOrderItemsDB.products_order_id == productOrderId).all()
        return orderItems

    def getProductsOrderItemsWithSession(self, db: Session, productOrderId: int, userId: int):
        if productOrderId is None:
                return None
        orderItems = db.query(ProductsOrderItemsDB).filter(ProductsOrderItemsDB.products_order_id == productOrderId, ProductsOrderItemsDB.users_id == userId).all()
        return orderItems

    def updateProductsOrderItemsById(self, productOrderItemsId: int):
        with getDB() as db:
            if productOrderItemsId is None:
                return None
            orderItem = db.query(ProductsOrderItemsDB).filter(ProductsOrderItemsDB.id == productOrderItemsId).first()
            orderItem.updated_at = getCurrentTime()
            db.commit()
        return orderItem

    def updateProductsOrderItemsByIdWithSession(self, db: Session, productOrderItemsId: int):
        if productOrderItemsId is None:
            return None
        orderItem = db.query(ProductsOrderItemsDB).filter(ProductsOrderItemsDB.id == productOrderItemsId).first()
        orderItem.updated_at = getCurrentTime()
        return orderItem