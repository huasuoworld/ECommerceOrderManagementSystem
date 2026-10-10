from sqlalchemy import Column, Integer, String, Boolean
from .SQLiteDB import Base, getDB
from ..Models.FrontEndReponseModel import PageDataReponseModel

class ProductsShoppingCartDB(Base):
    __tablename__ = 'products_shopping_cart'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer)
    users_id = Column(Integer)
    product_name = Column(String)
    product_code = Column(String)
    product_price = Column(Integer)
    product_discount = Column(Integer)
    product_img_url = Column(String)
    quantity = Column(Integer)
    created_at = Column(String)
    updated_at = Column(String)

    def queryProductsShoppingCartByUserId(self, userId) -> PageDataReponseModel:
        with getDB() as db:
            products = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId).all()
        return PageDataReponseModel(items = products)

    def addProductsShoppingCartByProductId(self, userId, product) -> PageDataReponseModel:
        with getDB() as db:
            product = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId, ProductsShoppingCartDB.product_id == self.product_id).first()
            if product == None:
                new_product = ProductsShoppingCartDB(**product)
                db.session.add(new_product)
                db.session.commit()
                db.session.refresh(new_product)
            products = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId).all()
        return PageDataReponseModel(items = products)

    def delProductsShoppingCartByProductId(self, userId, product) -> PageDataReponseModel:
            with getDB() as db:
                product = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId, ProductsShoppingCartDB.product_id == self.product_id).first()
                if product != None:
                    new_product = ProductsShoppingCartDB(**product)
                    db.session.add(new_product)
                    db.session.commit()
                    db.session.refresh(new_product)
                products = db.query(ProductsShoppingCartDB).filter(ProductsShoppingCartDB.users_id == userId).all()
            return PageDataReponseModel(items = products)