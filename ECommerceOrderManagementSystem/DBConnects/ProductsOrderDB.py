from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .NewBaseDB import NewBaseDB
from ..Models.ProductsOrderModel import ProductsOrderModel
from .SQLiteDB import getDB
from ..CommonUtils.ConstantUtil import DBExcludeColumnsWithoutId, getCurrentTime

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

    def createProductsOrder(self, db: Session, productsOrderModel: ProductsOrderModel) -> "ProductsOrderDB":
        productsOrderData = productsOrderModel.model_dump(exclude = DBExcludeColumnsWithoutId)
        timestamp = getCurrentTime()
        productsOrderDBData = ProductsOrderDB(**productsOrderData)
        productsOrderDBData.created_at = timestamp
        productsOrderDBData.updated_at = timestamp
        db.add(productsOrderDBData)
        db.flush()
        return productsOrderDBData

    def getOrderByUserId(self, userId: int):
        with getDB() as db:
            return db.query(ProductsOrderDB).filter(
                ProductsOrderDB.users_id == userId).order_by(ProductsOrderDB.id.desc()).all()

    def getOrderById(self, orderId: int):
        with getDB() as db:
            order = db.query(ProductsOrderDB).filter(ProductsOrderDB.id == orderId).first()
        return order

    def getOrderByIdAndUserIdWithSession(self, db: Session, orderId: int, userId: int):
        return db.query(ProductsOrderDB).filter(ProductsOrderDB.id == orderId, ProductsOrderDB.users_id == userId).first()

    def updateOrderById(self, orderId: int, orderStatus: str, paymentStatus: str):
        with getDB() as db:
            order = db.query(ProductsOrderDB).filter(ProductsOrderDB.id == orderId).first()
            order.updated_at = getCurrentTime()
            order.order_status = orderStatus
            order.payment_status = paymentStatus
        return order

    def updateOrderByIdWithSession(self, db: Session, orderId: int, orderStatus: str, paymentStatus: str):
        order = db.query(ProductsOrderDB).filter(ProductsOrderDB.id == orderId).first()
        order.updated_at = getCurrentTime()
        order.order_status = orderStatus
        order.payment_status = paymentStatus
        return order