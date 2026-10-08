from sqlalchemy import create_engine, Column, Integer, String
from .SQLiteDB import Base

class ProductsOrderDB(Base):
    __tablename__ = 'products_order'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    order_number = Column(String)
    order_amount = Column(Integer)
    order_discount_price = Column(Integer)
    order_payment_amount = Column(Integer)
    order_freight_price = Column(Integer)
    order_status = Column(String)
    created_at = Column(String)
    updated_at = Column(String)