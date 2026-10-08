from sqlalchemy import create_engine, Column, Integer, String
from .SQLiteDB import Base

class ProductsDB(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String)
    category_code = Column(String)
    brand_name = Column(String)
    brand_code = Column(String)
    product_name = Column(String)
    product_code = Column(String)
    product_price = Column(Integer)
    product_size = Column(String)
    product_color = Column(String)
    product_sub_name = Column(String)
    product_description = Column(String)
    product_img_url = Column(String)
    product_status = Column(String)
    created_at = Column(String)
    updated_at = Column(String)