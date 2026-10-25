from typing import Optional

from .UsersBaseModel import UsersBaseModel

class ProductsOrderModel(UsersBaseModel):
    # id: Optional[int] = None
    # created_at: Optional[str] = None
    # updated_at: Optional[str] = None
    users_id: int
    order_number: str
    order_amount: int
    order_discount_price: int
    order_product_price: int
    order_freight_price: int
    order_status: str
    payment_status: str

    class Config:
        from_attributes = True