from contextlib import contextmanager
import importlib

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ECommerceOrderManagementSystem.DBConnects.NewBaseDB import BaseDB
from ECommerceOrderManagementSystem.DBConnects.ProductsShoppingCartDB import ProductsShoppingCartDB
from ECommerceOrderManagementSystem.Models.ProductsShoppingCartModel import ProductsShoppingCartModel

cart_db_module = importlib.import_module(
    "ECommerceOrderManagementSystem.DBConnects.ProductsShoppingCartDB"
)


@pytest.fixture
def shopping_cart_db(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    BaseDB.metadata.create_all(engine, tables=[ProductsShoppingCartDB.__table__])
    session_factory = sessionmaker(bind=engine)

    @contextmanager
    def get_test_db():
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    monkeypatch.setattr(cart_db_module, "getDB", get_test_db)
    yield session_factory
    engine.dispose()


def test_add_and_update_cart_item_persist_timestamps(shopping_cart_db, monkeypatch):
    timestamps = iter(["2026-10-10 23:00:00", "2026-10-10 23:01:00"])
    monkeypatch.setattr(cart_db_module, "getCurrentTime", lambda: next(timestamps))
    cart_db = ProductsShoppingCartDB()

    def cart_item(quantity):
        return ProductsShoppingCartModel(
            users_id=7,
            product_id=1,
            products_discount_id=1,
            products_inventory_id=1,
            product_name="Test Jacket",
            product_code="J-1",
            product_price=699,
            discount_price=100,
            products_quantity=quantity,
            unit_price=599,
            products_total_price=599 * quantity,
        )

    cart_db.addProductsShoppingCartByProductId(7, cart_item(1))
    cart_db.addProductsShoppingCartByProductId(7, cart_item(2))

    with shopping_cart_db() as session:
        stored_item = session.query(ProductsShoppingCartDB).one()
        assert stored_item.products_quantity == 3
        assert stored_item.created_at == "2026-10-10 23:00:00"
        assert stored_item.updated_at == "2026-10-10 23:01:00"
