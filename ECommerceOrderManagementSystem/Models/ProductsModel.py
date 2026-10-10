from .NewBaseModel import NewBaseModel

class ProductsModel(NewBaseModel):
    category_name = str
    category_code = str
    brand_name = str
    brand_code = str
    product_name = str
    product_code = str
    product_price = int
    product_size = str
    product_color = str
    product_sub_name = str
    product_description = str
    product_img_url = str
    product_status = str
    product_discount = int

    class Config:
            from_attributes = True