from sqlalchemy import Column, Integer, String, Boolean
from typing import List
from .SQLiteDB import getDB
from .NewBaseDB import NewBaseDB
from ..Models.UsersPermissionRulesModel import UsersPermissionRulesModel
from ..CommonUtils.ConstantUtil import UserStatusActive, getCurrentTime, AdminPermission

class UsersPermissionRulesDB(NewBaseDB):
    __tablename__ = 'users_permission_rules'

    users_id = Column(Integer)
    permission_subject_path = Column(String)
    permission_resource_path = Column(String)
    permission_action = Column(String)
    permission_status = Column(String)
    subscription_type = Column(Boolean)

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

    def isAdminAndSubscribed(self, usersId: int) -> UsersPermissionRulesModel:
        with getDB() as db:
            usersPermissionRuleDBData = db.query(UsersPermissionRulesDB).filter(
                UsersPermissionRulesDB.users_id == usersId,
                UsersPermissionRulesDB.permission_subject_path == AdminPermission,
                UsersPermissionRulesDB.permission_status == UserStatusActive,
                UsersPermissionRulesDB.subscription_type == True
            ).first()
            if usersPermissionRuleDBData is None:
                return None
            return UsersPermissionRulesModel.model_validate(usersPermissionRuleDBData)

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
            