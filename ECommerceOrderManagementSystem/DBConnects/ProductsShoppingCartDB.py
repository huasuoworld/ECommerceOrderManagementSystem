from sqlalchemy import Column, Integer, String
from .SQLiteDB import getDB
from .NewBaseDB import NewBaseDB
from ..Models.ProductsShoppingCartModel import ProductsShoppingCartModel

class ProductsShoppingCartDB(NewBaseDB):
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

    #add shopping cart's items 
    def addProductsShoppingCartByProductId(self, userId: int, productShoppingCart: ProductsShoppingCartModel):
        productData = productShoppingCart.model_dump(exclude={"unit_price", "products_total_price"})
        with getDB() as db:
            productDBData = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId, ProductsShoppingCartDB.product_id == productData["product_id"]).first()
            if productDBData is None:
                newProduct = ProductsShoppingCartDB(**productData, users_id=userId)
                db.add(newProduct)
            else:
                productDBData.products_quantity += productData["products_quantity"]
            db.commit()

            products = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId).all()
        return products
    
    #update shopping cart's items by userId, productID
    def updateProductsShoppingCartQuantity(self, userId, productId, quantity: int):
        with getDB() as db:
            productDBData = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId, ProductsShoppingCartDB.product_id == productId).first()
            if productDBData is None:
                raise KeyError(productId)
            productDBData.products_quantity = quantity
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