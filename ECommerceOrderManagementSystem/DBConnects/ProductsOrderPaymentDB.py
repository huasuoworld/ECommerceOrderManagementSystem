from sqlalchemy import create_engine, Column, Integer, String
from .UsersBaseDB import UsersBaseDB
from ..Models import ProductsOrderPaymentModel
from .SQLiteDB import getDB

class ProductsOrderPaymentDB(UsersBaseDB):
    __tablename__ = 'products_order_payment'

    products_order_id = Column(Integer)
    users_id = Column(Integer)
    payment_number = Column(String)
    payment_channel = Column(String, default="CIBC")
    payment_type = Column(String, default="ONLINE")
    payment_amount = Column(Integer)
    payment_order_number = Column(String)
    payment_status = Column(String)

    #create productsOrderItems into database
    def createProductsOrderPayment(productsOrderPaymentModel: ProductsOrderPaymentModel):
        with getDB as db:
            productsOrderPaymentDBData = ProductsOrderPaymentDB(**productsOrderPaymentModel)
            db.add(productsOrderPaymentDBData)
            db.commit()
        return ProductsOrderPaymentModel.model_validate(productsOrderPaymentDBData)

    def getProductsOrderPaymentById(productsOrderPaymentId: int):
        with getDB as db:
            productsOrderPaymentDBData = db.query(ProductsOrderPaymentDB).filter(ProductsOrderPaymentDB.id == productsOrderPaymentId).first()
        return ProductsOrderPaymentModel.model_validate(productsOrderPaymentDBData)