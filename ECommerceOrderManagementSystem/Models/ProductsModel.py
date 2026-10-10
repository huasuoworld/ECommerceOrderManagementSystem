from .NewBaseModel import NewBaseModel
from .FrontEndReponseModel import PageDataReponseModel

#products model
class ProductsModel(NewBaseModel):
    category_name: str
    category_code: str
    brand_name: str
    brand_code: str
    product_name: str
    product_code: str
    product_price: int
    product_size: str
    product_color: str
    product_sub_name: str
    product_description: str
    product_img_url: str
    product_status: str

    class Config:
            from_attributes = True

    def getProductsIDList(productsPageList: PageDataReponseModel):
            if productsPageList.items == None:
                return None
            productsList = productsPageList.items
            return [product.id for product in productsList]