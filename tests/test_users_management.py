from contextlib import contextmanager
import asyncio
import importlib

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request
from starlette.responses import Response

from ECommerceOrderManagementSystem.APIGateways.Application import app
from ECommerceOrderManagementSystem.DBConnects.NewBaseDB import BaseDB
from ECommerceOrderManagementSystem.DBConnects.UsersDB import UsersDB
from ECommerceOrderManagementSystem.DBConnects.UsersPermissionRulesDB import UsersPermissionRulesDB
from ECommerceOrderManagementSystem.Models.UserProfileModel import UserProfileModel
from ECommerceOrderManagementSystem.Models.UsersModel import UsersModel
from ECommerceOrderManagementSystem.Services.UsersService import UsersService

users_db_module = importlib.import_module(
    "ECommerceOrderManagementSystem.DBConnects.UsersDB"
)
permission_db_module = importlib.import_module(
    "ECommerceOrderManagementSystem.DBConnects.UsersPermissionRulesDB"
)
users_management_api_module = importlib.import_module(
    "ECommerceOrderManagementSystem.APIGateways.UsersManagementAPI"
)
users_api_module = importlib.import_module(
    "ECommerceOrderManagementSystem.APIGateways.UsersAPI"
)
api_gateway_module = importlib.import_module(
    "ECommerceOrderManagementSystem.APIGateways.APIGatewayDefine"
)
user_login_service_module = importlib.import_module(
    "ECommerceOrderManagementSystem.Services.UserLoginService"
)


@pytest.fixture
def users_database(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    BaseDB.metadata.create_all(
        engine,
        tables=[UsersDB.__table__, UsersPermissionRulesDB.__table__],
    )
    session_factory = sessionmaker(bind=engine)

    @contextmanager
    def get_test_db():
        session = session_factory()
        try:
            yield session
        finally:
            session.close()

    monkeypatch.setattr(users_db_module, "getDB", get_test_db)
    monkeypatch.setattr(permission_db_module, "getDB", get_test_db)
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


def test_list_users_returns_requested_page_without_passwords(users_database):
    with users_database() as session:
        session.add_all([
            UsersDB(username=f"user-{index}", password="secret", display_name=f"User {index}",
                    user_email=f"user-{index}@example.test")
            for index in range(1, 4)
        ])
        session.commit()

    page = UsersService().listUsers(
        UserProfileModel.model_construct(page_number=2, page_size=2)
    )

    assert page.page_number == 2
    assert page.page_size == 2
    assert page.total_items == 3
    assert page.total_pages == 2
    assert [user.username for user in page.items] == ["user-3"]
    assert all("password" not in user.model_dump() for user in page.items)


def test_list_users_requires_management_permission(users_database):
    with users_database() as session:
        session.add(UsersDB(
            username="viewer",
            password="secret",
            display_name="Viewer",
            user_email="viewer@example.test",
        ))
        session.commit()
        user_id = session.query(UsersDB.id).filter_by(username="viewer").scalar()

    with pytest.raises(HTTPException) as error:
        asyncio.run(users_management_api_module.listUsers(
            user=UsersModel(id=user_id, username="viewer", password="secret")
        ))

    assert error.value.status_code == 403


def test_list_users_allows_user_with_management_permission(users_database):
    with users_database() as session:
        session.add(UsersDB(
            username="admin",
            password="secret",
            display_name="Admin",
            user_email="admin@example.test",
        ))
        session.commit()
        user_id = session.query(UsersDB.id).filter_by(username="admin").scalar()
        session.add(UsersPermissionRulesDB(
            users_id=user_id,
            permission_subject_path="/admin",
            permission_resource_path="/usersManagement",
            permission_action="GET,POST,DELETE,PATCH,PUT",
            permission_status="ALLOW",
        ))
        session.commit()

    page = asyncio.run(users_management_api_module.listUsers(
        page_number=1,
        page_size=10,
        user=UsersModel(id=user_id, username="admin", password="secret"),
    ))

    assert page.total_items == 1
    assert page.items[0].username == "admin"


def test_user_management_routes_are_registered():
    route_paths = {route.path for route in app.routes}

    assert "/users/me" in route_paths
    assert "/usersManagement" in route_paths
    assert "/management/users/listUsers" in route_paths


def test_login_authenticates_user_and_returns_management_redirect(
    users_database, monkeypatch
):
    with users_database() as session:
        session.add(UsersDB(
            username="login-test",
            password="test-password",
            display_name="Login Test",
        ))
        session.commit()
        user_id = session.query(UsersDB.id).filter_by(
            username="login-test"
        ).scalar()
        session.add(UsersPermissionRulesDB(
            users_id=user_id,
            permission_subject_path="/admin",
            permission_resource_path="/usersManagement",
            permission_action="GET",
            permission_status="ALLOW",
        ))
        session.commit()

    cached_sessions = []
    monkeypatch.setattr(
        user_login_service_module,
        "setSessionCache",
        lambda session_id, user: cached_sessions.append((session_id, user)),
    )

    response = asyncio.run(users_api_module.login(
        UsersModel(username="login-test", password="test-password")
    ))

    assert response.status == 200
    assert response.http_url == "/usersManagement"
    assert response.session_id
    assert len(cached_sessions) == 1
    assert cached_sessions[0][1].username == "login-test"
    assert cached_sessions[0][1].password == "test-password"


def test_login_rejects_invalid_password(users_database, monkeypatch):
    with users_database() as session:
        session.add(UsersDB(username="login-test", password="test-password"))
        session.commit()

    cached_sessions = []
    monkeypatch.setattr(
        user_login_service_module,
        "setSessionCache",
        lambda session_id, user: cached_sessions.append((session_id, user)),
    )

    response = asyncio.run(users_api_module.login(
        UsersModel(username="login-test", password="wrong-password")
    ))

    assert response.status != 200
    assert cached_sessions == []


def test_login_without_permission_redirect_uses_default_destination(
    users_database, monkeypatch
):
    with users_database() as session:
        session.add(UsersDB(username="seller-test", password="test-password"))
        session.commit()

    monkeypatch.setattr(
        user_login_service_module,
        "setSessionCache",
        lambda session_id, user: None,
    )

    response = asyncio.run(users_api_module.login(
        UsersModel(username="seller-test", password="test-password")
    ))

    assert response.status == 200
    assert response.session_id
    assert response.http_url is None


def test_login_with_seller_permission_redirects_to_products_management(
    users_database, monkeypatch
):
    with users_database() as session:
        session.add(UsersDB(username="seller-test", password="test-password"))
        session.commit()
        user_id = session.query(UsersDB.id).filter_by(
            username="seller-test"
        ).scalar()
        session.add(UsersPermissionRulesDB(
            users_id=user_id,
            permission_subject_path="/seller",
            permission_resource_path="/",
            permission_action="ALLOW",
            permission_status="ALLOW",
        ))
        session.commit()

    monkeypatch.setattr(
        user_login_service_module,
        "setSessionCache",
        lambda session_id, user: None,
    )

    response = asyncio.run(users_api_module.login(
        UsersModel(username="seller-test", password="test-password")
    ))

    assert response.status == 200
    assert response.http_url == "/productsManagement"


def test_login_endpoint_is_available_without_session():
    request = Request({
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": "/users/login",
        "raw_path": b"/users/login",
        "query_string": b"",
        "root_path": "",
        "headers": [],
        "client": ("test-client", 12345),
        "server": ("test-server", 80),
    })
    called_paths = []

    async def call_next(request):
        called_paths.append(request.url.path)
        return Response()

    response = asyncio.run(
        api_gateway_module.permissionCheck(request, call_next)
    )

    assert response.status_code == 200
    assert called_paths == ["/users/login"]
