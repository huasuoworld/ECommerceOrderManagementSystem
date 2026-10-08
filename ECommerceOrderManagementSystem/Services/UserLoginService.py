import logging

from ..DBConnects.SQLiteDB import SessionLocal
from ..DBConnects.UsersDB import UsersDB

logger = logging.getLogger(__name__)

class UserLoginService(object):
    def __init__(self):
        self.db = SessionLocal()

    def login(self, username: str, password: str) -> bool:
        user = self.db.query(UsersDB).filter(UsersDB.username == username).first()
        logger.info("Login user lookup completed; user_found=%s", user is not None)
        if user and user.password == password:
            return True
        return False