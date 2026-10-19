from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .NewBaseDB import NewBaseDB
from ..Models import ProductsOrderPaymentModel
from .SQLiteDB import getDB
from ..CommonUtils.ConstantUtil import DBExcludeColumnsWithoutId

class ProductsOrderPaymentDB(NewBaseDB):
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
    def createProductsOrderPaymentWithSession(db: Session, productsOrderPaymentModel: ProductsOrderPaymentModel):
        productsOrderPayment = productsOrderPaymentModel.model_dump(exclude = DBExcludeColumnsWithoutId)
        productsOrderPaymentDBData = ProductsOrderPaymentDB(**productsOrderPayment)
        db.add(productsOrderPaymentDBData)
        db.commit()
        return ProductsOrderPaymentModel.model_validate(productsOrderPaymentDBData)

    def getProductsOrderPaymentByIdWithSession(db: Session, productsOrderPaymentId: int):
        productsOrderPaymentDBData = db.query(ProductsOrderPaymentDB).filter(ProductsOrderPaymentDB.id == productsOrderPaymentId).first()
        return ProductsOrderPaymentModel.model_validate(productsOrderPaymentDBData)