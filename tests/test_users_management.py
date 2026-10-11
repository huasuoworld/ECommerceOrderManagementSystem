from contextlib import contextmanager
import importlib

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ECommerceOrderManagementSystem.APIGateways.Application import app
from ECommerceOrderManagementSystem.DBConnects.NewBaseDB import BaseDB
from ECommerceOrderManagementSystem.DBConnects.UsersDB import UsersDB
from ECommerceOrderManagementSystem.Services.UsersService import UsersService

users_db_module = importlib.import_module(
    "ECommerceOrderManagementSystem.DBConnects.UsersDB"
)


@pytest.fixture
def users_database(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    BaseDB.metadata.create_all(engine, tables=[UsersDB.__table__])
    session_factory = sessionmaker(bind=engine)

    @contextmanager
    def get_test_db():
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    monkeypatch.setattr(users_db_module, "getDB", get_test_db)
    yield session_factory
    engine.dispose()


def test_current_user_profile_excludes_password(users_database):
    with users_database() as session:
        session.add(UsersDB(
            username="profile-test",
            password="test-only-password",
            display_name="Profile Test",
            user_email="profile@example.test",
            user_phone="555-0100",
            user_status="Active",
        ))
        session.commit()
        user_id = session.query(UsersDB.id).filter_by(username="profile-test").scalar()

    profile = UsersService().getUserProfile(user_id)

    assert profile is not None
    assert profile.username == "profile-test"
    assert profile.display_name == "Profile Test"
    assert "password" not in profile.model_dump()


def test_current_user_profile_returns_none_for_unknown_user(users_database):
    assert UsersService().getUserProfile(999) is None


def test_user_management_routes_are_registered():
    route_paths = {route.path for route in app.routes}

    assert "/users/me" in route_paths
    assert "/usersManagement" in route_paths
