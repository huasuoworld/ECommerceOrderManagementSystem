from sqlalchemy import create_engine, Column, Integer, String
from .SQLiteDB import Base

class ProductsOrderPaymentDB(Base):
    __tablename__ = 'products_order_payment'

    id = Column(Integer, primary_key=True, index=True)
    products_order_id = Column(Integer)
    users_id = Column(Integer)
    payment_number = Column(String)
    payment_channel = Column(String)
    payment_type = Column(String)
    payment_amount = Column(Integer)
    payment_order_number = Column(String)
    payment_status = Column(String)
    created_at = Column(String)
    updated_at = Column(String)