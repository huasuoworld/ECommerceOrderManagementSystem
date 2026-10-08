from sqlalchemy import create_engine, Column, Integer, String
from .SQLiteDB import Base

class ProductsOrderItemsDB(Base):
    __tablename__ = 'products_order_items'

    id = Column(Integer, primary_key=True, index=True)
    products_order_id = Column(Integer)
    users_id = Column(Integer)
    products_id = Column(Integer)
    products_inventory_id = Column(Integer)
    item_quantity = Column(Integer)
    item_ordder_number = Column(String)
    item_origin_price = Column(Integer)
    item_real_price = Column(Integer)
    created_at = Column(String)
    updated_at = Column(String)