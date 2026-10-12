from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from typing import Optional
from .SQLiteDB import getDB
from .UsersBaseDB import UsersBaseDB
from ..Models.ProductsShoppingCartModel import ProductsShoppingCartModel
from ..CommonUtils.ConstantUtil import DBExcludeShoppingCartColumns, getCurrentTime

class ProductsShoppingCartDB(UsersBaseDB):
    __tablename__ = 'products_shopping_cart'

    product_id = Column(Integer)
    users_id = Column(Integer)
    products_discount_id = Column(Integer)
    products_inventory_id = Column(Integer)
    product_name = Column(String)
    product_code = Column(String)
    product_price = Column(Integer)
    discount_price = Column(Integer)
    product_img_url = Column(String)
    products_quantity = Column(Integer)

    #get shopping cart's items by userId
    def queryProductsShoppingCartByUserId(self, userId):
        with getDB() as db:
            products = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId).all()
        return products

        #get shopping cart's items by userId
    def queryProductsShoppingCartByUserIdWithSession(self, userId: int, db: Optional[Session] = None):
        if db is not None:
            return db.query(ProductsShoppingCartDB).filter(
                ProductsShoppingCartDB.users_id == userId
            ).all()
        with getDB() as session:
            return session.query(ProductsShoppingCartDB).filter(
                ProductsShoppingCartDB.users_id == userId
            ).all()

    #add shopping cart's items 
    def addProductsShoppingCartByProductId(self, userId: int, productShoppingCart: ProductsShoppingCartModel):
        productShoppingCart.users_id = userId
        productData = productShoppingCart.model_dump(
            exclude=DBExcludeShoppingCartColumns
        )
        productData["users_id"] = userId
        with getDB() as db:
            productDBData = db.query(ProductsShoppingCartDB).filter(
                ProductsShoppingCartDB.users_id == userId,
                ProductsShoppingCartDB.product_id == productShoppingCart.product_id,
            ).first()
            timestamp = getCurrentTime()
            if productDBData is None:
                newProduct = ProductsShoppingCartDB(**productData)
                newProduct.created_at = timestamp
                newProduct.updated_at = timestamp
                db.add(newProduct)
            else:
                productDBData.updated_at = timestamp
                productDBData.products_quantity += productShoppingCart.products_quantity
            db.commit()

            products = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId).all()
        return products
    
    #update shopping cart's items by userId, productID
    def updateProductsShoppingCartQuantity(self, userId, productId, quantity: int):
        with getDB() as db:
            productDBData = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId, ProductsShoppingCartDB.product_id == productId).first()
            if productDBData is None:
                raise KeyError(productId)
            timestamp = getCurrentTime()
            productDBData.products_quantity = quantity
            productDBData.updated_at = timestamp
            db.commit()
            products = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId).all()
        return products

    #delete shopping cart's items by userId, productID
    def delProductsShoppingCartByProductId(self, userId, productID):
        with getDB() as db:
            productDBData = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId, ProductsShoppingCartDB.product_id == productID).first()
            if productDBData is None:
                raise KeyError(productID)
            db.delete(productDBData)
            db.commit()
            products = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId).all()
        return products

    #delete shopping cart's items by userId
    def delProductsShoppingCartByUserIdWithSession(self, db: Session, userId):
        db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId).delete(synchronize_session=False)