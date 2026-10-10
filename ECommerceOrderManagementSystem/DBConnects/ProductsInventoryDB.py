from sqlalchemy import create_engine, Column, Integer, String
from .NewBaseDB import NewBaseDB
from .SQLiteDB import getDB
from ..Models.FrontEndReponseModel import PageDataReponseModel
from ..Models.ProductsInventoryModel import ProductsInventoryModel
from typing import List

class ProductsInventoryDB(NewBaseDB):
    __tablename__ = 'products_inventory'

    product_id = Column("products_id", Integer)
    warehouse_name = Column(String)
    warehouse_code = Column(String)
    inventory_stock = Column(Integer)
    inventory_reserved_stock = Column(Integer)
    inventory_available_stock = Column(Integer)
    inventory_status = Column(String)


    #create a new product Inventory
    def createProductInventory(self, productInventoryData):
        with getDB() as db:
            newProductInventory = ProductsInventoryDB(**productInventoryData)
            db.session.add(newProductInventory)
            db.session.commit()
            db.session.refresh(newProductInventory)
            return newProductInventory
        
    #get a product inventory by its ID
    def getProductInventoryById(self, productInventoryId) -> ProductsInventoryModel:
        with getDB() as db:
            productInventory = db.query(ProductsInventoryDB).filter(ProductsInventoryDB.id == productInventoryId).first()
        return ProductsInventoryModel.model_validate(productInventory) if productInventory else None
    
    #list all products inventory with pagination
    def listProductsInventory(self, productInventory: ProductsInventoryModel) -> PageDataReponseModel:
        with getDB() as db:
            total = db.query(ProductsInventoryDB).count()
            offset = (productInventory.page_number - 1) * productInventory.page_size
            products = db.query(ProductsInventoryDB).filter(ProductsInventoryDB.inventory_available_stock > 0).offset(offset).limit(productInventory.page_size).all()
        return PageDataReponseModel(
            page_number = productInventory.page_number,
            page_size = productInventory.page_size,
            total_items = total,
            total_pages = (total + productInventory.page_size - 1) // productInventory.page_size,
            items = [ProductsInventoryModel.model_validate(product) for product in products]
        )

    #list all productsInventory by IDs
    def listProductsInventoryByIDs(self, productIDs: List) -> PageDataReponseModel:
        with getDB() as db:
            productsInventoryList = db.query(ProductsInventoryDB).filter(ProductsInventoryDB.product_id.in_(productIDs), ProductsInventoryDB.inventory_available_stock > 0).all()
        return PageDataReponseModel(
            items=[ProductsInventoryModel.model_validate(item) for item in productsInventoryList]
        )