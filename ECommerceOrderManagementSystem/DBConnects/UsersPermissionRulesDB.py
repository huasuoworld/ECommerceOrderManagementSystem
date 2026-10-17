from sqlalchemy import Column, Integer, String
from typing import List
from .SQLiteDB import getDB
from .NewBaseDB import NewBaseDB
from ..Models.UsersPermissionRulesModel import UsersPermissionRulesModel
from ..CommonUtils.ConstantUtil import UserStatusActive, getCurrentTime

class UsersPermissionRulesDB(NewBaseDB):
    __tablename__ = 'users_permission_rules'

    users_id = Column(Integer)
    permission_subject_path = Column(String)
    permission_resource_path = Column(String)
    permission_action = Column(String)
    permission_status = Column(String)

    def hasPermission(self, usersId: int, subjectPath: str) -> List[UsersPermissionRulesModel]:
        with getDB() as db:
            usersPermissionRules = db.query(UsersPermissionRulesDB).filter(
                UsersPermissionRulesDB.users_id == usersId,
                UsersPermissionRulesDB.permission_subject_path == subjectPath,
                UsersPermissionRulesDB.permission_status == UserStatusActive,
            ).all()
            return [
                UsersPermissionRulesModel.model_validate(rule)
                for rule in usersPermissionRules
            ]

    def getPermissionByUserId(self, usersId: int) -> List[UsersPermissionRulesModel]:
        with getDB() as db:
            usersPermissionRules = db.query(UsersPermissionRulesDB).filter(
                UsersPermissionRulesDB.users_id == usersId,
                UsersPermissionRulesDB.permission_status == UserStatusActive,
            ).all()
            return [
                UsersPermissionRulesModel.model_validate(rule)
                for rule in usersPermissionRules
            ]

    def updatePermission(self, usersPermissionRulesModel: UsersPermissionRulesModel):
        with getDB() as db:
            usersPermissionRules = db.query(UsersPermissionRulesDB).filter(
                UsersPermissionRulesDB.users_id == usersPermissionRulesModel.users_id).first()
            if usersPermissionRules == None:
                return None
            timestamp = getCurrentTime()
            usersPermissionRules.updated_at = timestamp
            usersPermissionRules.permission_status = usersPermissionRulesModel.permission_status
            db.commit()
            return usersPermissionRules
            