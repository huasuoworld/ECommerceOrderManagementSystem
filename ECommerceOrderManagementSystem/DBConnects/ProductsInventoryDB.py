from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from .UsersBaseDB import UsersBaseDB
from .SQLiteDB import getDB
from ..Models.FrontEndReponseModel import PageDataReponseModel, ErrorResponseException
from ..Models.ProductsInventoryModel import ProductsInventoryModel
from ..CommonUtils.ConstantUtil import InsufficientAvailableStockError, InsufficientAvailableStockMessage, InsufficientInventoryStockError, InsufficientInventoryStockMessage, InsufficientReservedStockError, InsufficientReservedStockMessage, getCurrentTime


class ProductsInventoryDB(UsersBaseDB):
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
    def getProductInventoryByProductId(self, productId) -> ProductsInventoryModel:
        with getDB() as db:
            productInventory = db.query(ProductsInventoryDB).filter(ProductsInventoryDB.product_id == productId).first()
        return ProductsInventoryModel.model_validate(productInventory) if productInventory else None
        
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
            items=[ProductsInventoryModel.model_validate(item) for item in productsInventoryList])

    def getProductInventoryByProductIdWithSession(self, db: Session, productId):
        return db.query(ProductsInventoryDB).filter(ProductsInventoryDB.product_id == productId).first()

    #update inventory after order was confirmed
    def lockStockWithSession(self, db: Session, productId: int, numberOfReservedStock: int):
        #1. find the inventory
        productInventory = db.query(ProductsInventoryDB).filter(ProductsInventoryDB.product_id == productId).first()
        #if stock is not available then throw exception
        if numberOfReservedStock > productInventory.inventory_available_stock:
            raise ErrorResponseException(InsufficientAvailableStockError, InsufficientAvailableStockMessage)
        #2. reduce available stock
        productInventory.inventory_available_stock = productInventory.inventory_available_stock - numberOfReservedStock
        #3. increase reserved stock
        productInventory.inventory_reserved_stock = productInventory.inventory_reserved_stock + numberOfReservedStock
        productInventory.updated_at = getCurrentTime()
        return productInventory

    #update inventory after payment
    def releaseReservedStockWithSession(self, db: Session, productId: int, numberOfReservedStock: int):
        #1. find the inventory
        productInventory = db.query(ProductsInventoryDB).filter(ProductsInventoryDB.product_id == productId).first()
        #if stock is not available then throw exception
        if numberOfReservedStock > productInventory.inventory_available_stock:
            raise ErrorResponseException(InsufficientAvailableStockError, InsufficientAvailableStockMessage)
        elif numberOfReservedStock > productInventory.inventory_stock:
            raise ErrorResponseException(InsufficientInventoryStockError, InsufficientInventoryStockMessage)
        #2. reduce reserved stock
        productInventory.inventory_reserved_stock = productInventory.inventory_reserved_stock - numberOfReservedStock
        #3. reduce inventory stock
        productInventory.inventory_stock = productInventory.inventory_stock - numberOfReservedStock
        productInventory.updated_at = getCurrentTime()
        return productInventory

    #update inventory after order was canceled
    def releaseStockWithSession(self, db: Session, productId: int, numberOfReservedStock: int):
        #1. find the inventory
        productInventory = db.query(ProductsInventoryDB).filter(ProductsInventoryDB.product_id == productId).first()
        if numberOfReservedStock > productInventory.inventory_reserved_stock:
            raise ErrorResponseException(InsufficientReservedStockError, InsufficientReservedStockMessage)
        #2. reduce reserved stock
        productInventory.inventory_reserved_stock = productInventory.inventory_reserved_stock - numberOfReservedStock
        #3. increase available stock
        productInventory.inventory_available_stock = productInventory.inventory_available_stock + numberOfReservedStock
        productInventory.updated_at = getCurrentTime()
        return productInventory