from sqlalchemy import create_engine, Column, Integer, String
from .SQLiteDB import getDB
from ..Models.ProductsDiscountInventoryModel import ProductsDiscountInventoryModel
from ..Models.ProductsModel import ProductsModel
from ..Models.FrontEndReponseModel import PageDataReponseModel
from .NewBaseDB import NewBaseDB
from typing import List

class ProductsDB(NewBaseDB):
    __tablename__ = 'products'

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

    #create a new product
    def createProduct(self, product_data):
        with getDB() as db:
            new_product = ProductsDB(**product_data)
            db.session.add(new_product)
            db.session.commit()
            db.session.refresh(new_product)
            return new_product
    #get a product by its ID
    def getProductById(self, productId) -> ProductsModel:
        with getDB() as db:
            product = db.query(ProductsDB).filter(ProductsDB.id == productId).first()
            if product == None:
                return None
        return ProductsModel.model_validate(product) if product else None

    #list all products with pagination
    def listProducts(self, product: ProductsDiscountInventoryModel) -> PageDataReponseModel:
        with getDB() as db:
            total = db.query(ProductsDB).count()
            offset = (product.page_number - 1) * product.page_size
            products = db.query(ProductsDB).offset(offset).limit(product.page_size).all()
        return PageDataReponseModel(
            page_number = product.page_number,
            page_size = product.page_size,
            total_items = total,
            total_pages = (total + product.page_size - 1) // product.page_size,
            items = [ProductsDiscountInventoryModel.model_validate(product) for product in products]
        )
    #list all products by IDs
    def listProductsByIDs(self, productIDs: List) -> PageDataReponseModel:
        with getDB as db:
            products = db.query(ProductsDB).filter(ProductsDB.id.in_(productIDs)).all()
        return PageDataReponseModel(ProductsDiscountInventoryModel.model_validate(product) for product in products)