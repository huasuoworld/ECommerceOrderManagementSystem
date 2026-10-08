from DBConnects.SQLiteDB import engine, SessionLocal
from DBConnects.UsersDB import UsersDB
from datetime import datetime

class UserLoginService(object):
    def __init__(self):
        self.db = SessionLocal()

    def create_user(self, username: str, password: str, display_name: str, user_email: str, user_phone: str, user_status: str) -> UsersDB:
        try:
            # 测试插入用户
            new_user = self.db.query(UsersDB).filter_by(username=username).first()
            if new_user is None:
                new_user = UsersDB(
                    username=username,
                    password=password,
                    display_name=display_name,
                    user_email=user_email,
                    user_phone=user_phone,
                    user_status=user_status,
                    created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                self.db.add(new_user)
                self.db.commit()
                self.db.refresh(new_user)
    
            print(f"users ID={new_user.id}, Name={new_user.username}")
            return new_user    
        finally:
            self.db.close()
        