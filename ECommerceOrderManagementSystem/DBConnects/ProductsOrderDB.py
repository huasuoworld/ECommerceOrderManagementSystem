from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .NewBaseDB import NewBaseDB
from ..Models.ProductsOrderModel import ProductsOrderModel
from .SQLiteDB import getDB
from ..CommonUtils.ConstantUtil import DBExcludeColumns, getCurrentTime

class ProductsOrderDB(NewBaseDB):
    __tablename__ = 'products_order'

    users_id = Column(Integer)
    order_number = Column(String)
    order_amount = Column(Integer)
    order_discount_price = Column(Integer)
    order_product_price = Column(Integer)
    order_freight_price = Column(Integer)
    order_status = Column(String)
    payment_status = Column(String)

    def createProductsOrder(
        self,
        db: Session,
        productsOrderModel: ProductsOrderModel,
    ) -> "ProductsOrderDB":
        productsOrderData = productsOrderModel.model_dump(
            exclude=DBExcludeColumns | {"seller_id"}
        )
        timestamp = getCurrentTime()
        productsOrderData["created_at"] = timestamp
        productsOrderData["updated_at"] = timestamp
        productsOrderDBData = ProductsOrderDB(**productsOrderData)
        db.add(productsOrderDBData)
        db.flush()
        return productsOrderDBData

    def getOrderByUserId(self, userId: int):
        with getDB() as db:
            return db.query(ProductsOrderDB).filter(
                ProductsOrderDB.users_id == userId).order_by(ProductsOrderDB.id.desc()).all()