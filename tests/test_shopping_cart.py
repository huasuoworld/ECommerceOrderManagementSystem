import pytest

from ECommerceOrderManagementSystem.APIGateways.APIGatewayDefine import app
from ECommerceOrderManagementSystem.Services.ShoppingCartService import ShoppingCartService


@pytest.fixture(autouse=True)
def empty_mock_cart():
    ShoppingCartService._quantities.clear()
    yield
    ShoppingCartService._quantities.clear()


def test_cart_uses_discounted_price_for_subtotal():
    cart = ShoppingCartService()

    result = cart.add_item(product_id=1, quantity=2)

    assert result["item_count"] == 2
    assert result["subtotal"] == 1198
    assert result["items"][0]["unit_price"] == 599
    assert result["items"][0]["line_total"] == 1198


def test_cart_can_update_and_remove_items():
    cart = ShoppingCartService()
    cart.add_item(product_id=2)

    updated = cart.update_quantity(product_id=2, quantity=3)
    assert updated["item_count"] == 3
    assert updated["subtotal"] == 1377

    removed = cart.remove_item(product_id=2)
    assert removed == {"items": [], "item_count": 0, "subtotal": 0}


def test_cart_rejects_unknown_product_and_invalid_quantity():
    cart = ShoppingCartService()

    with pytest.raises(KeyError):
        cart.add_item(product_id=999)

    with pytest.raises(ValueError):
        cart.add_item(product_id=1, quantity=0)


def test_shopping_cart_routes_are_registered_on_api_app():
    routes = {
        (method, route.path)
        for route in app.routes
        for method in getattr(route, "methods", set())
    }

    assert ("GET", "/shopping-cart") in routes
    assert ("POST", "/shopping-cart/items") in routes
    assert ("PATCH", "/shopping-cart/items/{product_id}") in routes
    assert ("DELETE", "/shopping-cart/items/{product_id}") in routes
