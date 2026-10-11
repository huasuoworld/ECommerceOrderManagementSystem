from typing import Optional

from .NewBaseModel import NewBaseModel

class ProductsOrderItemsModel(NewBaseModel):
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    products_order_id: int
    users_id: int
    products_id: int
    products_discount_id: int
    products_inventory_id: int
    product_name: str
    product_code: str
    item_quantity: int
    item_ordder_number: str
    item_product_price: int
    item_discount_price: int
    item_unit_price: int

    class Config:
        from_attributes = True