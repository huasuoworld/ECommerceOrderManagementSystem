from sqlalchemy import create_engine, Column, Integer, String
from .SQLiteDB import Base

class ProductsInventoryDB(Base):
    __tablename__ = 'products_inventory'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    warehouse_name = Column(String)
    warehouse_code = Column(String)
    inventory_stock = Column(Integer)
    inventory_reserved_stock = Column(Integer)
    inventory_available_stock = Column(Integer)
    inventory_status = Column(String)
    created_at = Column(String)
    updated_at = Column(String)