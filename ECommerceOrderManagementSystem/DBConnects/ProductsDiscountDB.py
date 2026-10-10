from sqlalchemy import create_engine, Column, Integer, String
from .NewBaseDB import NewBaseDB
from typing import List
from .SQLiteDB import getDB
from ..Models.FrontEndReponseModel import PageDataReponseModel
from ..Models.ProductsDiscountModel import ProductsDiscountModel

class ProductsDiscountDB(NewBaseDB):
    __tablename__ = 'products_discount'

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

    #list all products by IDs
    def listProductsDiscountByProductsIDs(self, productIDs: List) -> PageDataReponseModel:
        with getDB() as db:
            productsDiscountList = db.query(ProductsDiscountDB).filter(ProductsDiscountDB.product_id.in_(productIDs), ProductsDiscountDB.discount_status == "Active").all()
        return PageDataReponseModel(
            items=[ProductsDiscountModel.model_validate(item) for item in productsDiscountList]
        )