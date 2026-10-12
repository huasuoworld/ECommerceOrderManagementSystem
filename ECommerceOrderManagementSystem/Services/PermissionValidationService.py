from ..DBConnects.UsersPermissionRulesDB import UsersPermissionRulesDB
from ..Models.UsersPermissionRulesModel import UsersPermissionRulesModel

class PermissionValidationService:
    def __init__(self):
            self.usersPermissionRulesDB = UsersPermissionRulesDB()

    def hasPermission(self, usersId: int, subjectPath: str) -> bool:
        if subjectPath == None:
            return False
        usersPermissionRulesList = self.usersPermissionRulesDB.hasPermission(usersId, subjectPath)
        if usersPermissionRulesList == None:
            return False
        orderItems = [usersPermissionRules.permission_subject_path for usersPermissionRules in usersPermissionRulesList]
        if subjectPath not in orderItems:
            return False
        return True