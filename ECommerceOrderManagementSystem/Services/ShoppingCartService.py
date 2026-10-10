from typing import Dict, List, TypedDict
from ..RedisCache.RedisConnect import r


class MockProduct(TypedDict):
    id: int
    product_name: str
    product_code: str
    product_price: int
    product_discount: int
    product_img_url: str


class ShoppingCartService:
    _quantities: Dict[int, int] = {}

    def get_cart(self) -> dict:
        items: List[dict] = []
        item_count = 0
        subtotal = 0

        for product_id, quantity in self._quantities.items():
            product = self._products[product_id]
            unit_price = max(0, product["product_price"] - product["product_discount"])
            line_total = unit_price * quantity
            items.append({
                **product,
                "quantity": quantity,
                "unit_price": unit_price,
                "line_total": line_total,
            })
            item_count += quantity
            subtotal += line_total

        return {
            "items": items,
            "item_count": item_count,
            "subtotal": subtotal,
        }

    def addItem(self, product_id: int, quantity: int = 1) -> dict:
        if product_id not in self._products:
            raise KeyError(product_id)
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        self._quantities[product_id] = self._quantities.get(product_id, 0) + quantity
        return self.get_cart()

    def updateQuantity(self, product_id: int, quantity: int) -> dict:
        if product_id not in self._quantities:
            raise KeyError(product_id)
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        self._quantities[product_id] = quantity
        return self.get_cart()

    def removeItem(self, product_id: int) -> dict:
        if product_id not in self._quantities:
            raise KeyError(product_id)
        del self._quantities[product_id]
        return self.get_cart()