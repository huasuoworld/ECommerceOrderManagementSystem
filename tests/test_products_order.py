from contextlib import contextmanager
import importlib

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ECommerceOrderManagementSystem.DBConnects.NewBaseDB import BaseDB
from ECommerceOrderManagementSystem.DBConnects.ProductsOrderDB import ProductsOrderDB
from ECommerceOrderManagementSystem.DBConnects.ProductsOrderItemsDB import ProductsOrderItemsDB
from ECommerceOrderManagementSystem.DBConnects.ProductsShoppingCartDB import ProductsShoppingCartDB
from ECommerceOrderManagementSystem.Models.ProductsOrderItemsModel import ProductsOrderItemsModel
from ECommerceOrderManagementSystem.Models.ProductsOrderModel import ProductsOrderModel
from ECommerceOrderManagementSystem.Services import ProductsOrderService as order_service_module
from ECommerceOrderManagementSystem.Services.ProductsOrderService import ProductsOrderService
from ECommerceOrderManagementSystem.DBConnects.ProductsOrderDB import ProductsOrderDB

products_order_db_module = importlib.import_module(
    "ECommerceOrderManagementSystem.DBConnects.ProductsOrderDB"
)


@pytest.fixture
def order_service_db(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    BaseDB.metadata.create_all(
        engine,
        tables=[
            ProductsOrderDB.__table__,
            ProductsOrderItemsDB.__table__,
            ProductsShoppingCartDB.__table__,
        ],
    )
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    @contextmanager
    def get_test_db():
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    monkeypatch.setattr(order_service_module, "getDB", get_test_db)
    monkeypatch.setattr(products_order_db_module, "getDB", get_test_db)
    yield session_factory
    engine.dispose()


def test_confirm_order_saves_order_and_clears_users_cart(order_service_db):
    with order_service_db() as session:
        session.add(ProductsShoppingCartDB(
            users_id=7,
            product_id=101,
            products_discount_id=4,
            products_inventory_id=6,
            product_name="Test Item",
            product_code="T-101",
            product_price=100,
            discount_price=15,
            products_quantity=2,
        ))
        session.commit()

    service = ProductsOrderService()
    created_order = service.confirmOrderByUserShoppingCart(7)

    assert created_order.order_amount == 170
    assert created_order.order_product_price == 200
    assert created_order.order_discount_price == 30
    assert created_order.order_number.startswith("ORD-")
    assert created_order.created_at is not None
    assert created_order.updated_at is not None
    assert len(service.getOrderByUserId(7)) == 1
    with order_service_db() as session:
        assert session.query(ProductsShoppingCartDB).filter_by(users_id=7).count() == 0
        stored_order = session.query(ProductsOrderDB).one()
        assert stored_order.created_at is not None
        assert stored_order.updated_at is not None
        order_item = session.query(ProductsOrderItemsDB).one()
        assert order_item.products_order_id == created_order.id
        assert order_item.item_quantity == 2
        assert order_item.created_at is not None
        assert order_item.updated_at is not None


def test_confirm_order_rejects_empty_cart(order_service_db):
    with pytest.raises(ValueError, match="cart is empty"):
        ProductsOrderService().confirmOrderByUserShoppingCart(7)


def test_order_database_writes_supply_missing_timestamps(order_service_db):
    order_model = ProductsOrderModel(
        users_id=7,
        order_number="ORD-test",
        order_amount=100,
        order_discount_price=0,
        order_product_price=100,
        order_freight_price=0,
        order_status="Unpaid",
        payment_status="Unpaid",
    )
    order_item_model = ProductsOrderItemsModel(
        products_order_id=1,
        users_id=7,
        products_id=101,
        products_discount_id=4,
        products_inventory_id=6,
        product_name="Test Item",
        product_code="T-101",
        item_quantity=1,
        item_ordder_number="ORD-test",
        item_product_price=100,
        item_discount_price=0,
        item_unit_price=100,
    )

    with order_service_db() as session:
        order = ProductsOrderDB().createProductsOrder(session, order_model)
        order_item_model.products_order_id = order.id
        ProductsOrderItemsDB().createProductsOrderItems(session, [order_item_model])
        session.commit()

        stored_order = session.query(ProductsOrderDB).one()
        stored_order_item = session.query(ProductsOrderItemsDB).one()
        assert stored_order.created_at is not None
        assert stored_order.updated_at is not None
        assert stored_order_item.created_at is not None
        assert stored_order_item.updated_at is not None
