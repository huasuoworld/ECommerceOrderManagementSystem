from typing import Optional

from pydantic import BaseModel


class ProductsShoppingCartModel(BaseModel):
    product_id: int
    products_discount_id: int
    products_inventory_id: int
    product_name: str
    product_code: str
    product_price: int
    discount_price: int
    product_img_url: Optional[str] = None
    products_quantity: int
    unit_price: int
    products_total_price: int