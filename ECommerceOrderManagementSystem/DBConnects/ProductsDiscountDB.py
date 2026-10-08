from sqlalchemy import create_engine, Column, Integer, String
from .SQLiteDB import Base

class ProductsDiscountDB(Base):
    __tablename__ = 'products_discount'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    discount_name = Column(String)
    discount_code = Column(String)
    discount_type = Column(String)
    discount_price = Column(Integer)
    discount_person_limit_stock = Column(Integer)
    discount_stock = Column(Integer)
    discount_start_time = Column(String)
    discount_end_time = Column(String)
    discount_status = Column(String)
    created_at = Column(String)
    updated_at = Column(String)