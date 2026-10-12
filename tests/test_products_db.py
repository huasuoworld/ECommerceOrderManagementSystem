from contextlib import contextmanager
import importlib

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ECommerceOrderManagementSystem.DBConnects.NewBaseDB import BaseDB
from ECommerceOrderManagementSystem.DBConnects.ProductsDB import ProductsDB
from ECommerceOrderManagementSystem.Models.ProductsDiscountInventoryModel import (
    ProductsDiscountInventoryModel,
)

products_db_module = importlib.import_module(
    "ECommerceOrderManagementSystem.DBConnects.ProductsDB"
)


@pytest.fixture
def products_database(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    BaseDB.metadata.create_all(engine, tables=[ProductsDB.__table__])
    session_factory = sessionmaker(bind=engine)

    @contextmanager
    def get_test_db():
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    monkeypatch.setattr(products_db_module, "getDB", get_test_db)
    yield session_factory
    engine.dispose()


def make_product(seller_id, name):
    return ProductsDB(
        seller_id=seller_id,
        category_name="Test",
        category_code="TEST",
        brand_name="Test Brand",
        brand_code="TEST",
        product_name=name,
        product_code=name.upper().replace(" ", "-"),
        product_price=100,
        product_size="M",
        product_color="Black",
        product_sub_name=name,
        product_description=name,
        product_img_url="",
        product_status="Active",
    )


def test_list_products_without_seller_id_returns_all_products(products_database):
    with products_database() as session:
        session.add_all([
            make_product("1", "Seller One Product"),
            make_product("2", "Seller Two Product"),
        ])
        session.commit()

    page = ProductsDB().listProducts(
        ProductsDiscountInventoryModel.model_construct(
            seller_id=None,
            page_number=1,
            page_size=10,
        )
    )

    assert page.total_items == 2
    assert {item.product_name for item in page.items} == {
        "Seller One Product",
        "Seller Two Product",
    }


def test_list_products_with_seller_id_filters_and_counts_matching_products(
    products_database,
):
    with products_database() as session:
        session.add_all([
            make_product("1", "Seller One Product"),
            make_product("2", "Seller Two Product"),
        ])
        session.commit()

    page = ProductsDB().listProducts(
        ProductsDiscountInventoryModel.model_construct(
            seller_id=1,
            page_number=1,
            page_size=10,
        )
    )

    assert page.total_items == 1
    assert [item.product_name for item in page.items] == ["Seller One Product"]
