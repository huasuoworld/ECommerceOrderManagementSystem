from .UsersBaseModel import UsersBaseModel

class ProductsDiscountModel(UsersBaseModel):
    product_id: int
    discount_name: str
    discount_code: str
    discount_type: str
    discount_price: int
    discount_person_limit_stock: int
    discount_stock: int
    discount_start_time: str
    discount_end_time: str
    discount_status: str

    class Config:
            from_attributes = True