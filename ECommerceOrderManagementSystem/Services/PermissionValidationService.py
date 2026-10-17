from typing import List
from ..DBConnects.UsersPermissionRulesDB import UsersPermissionRulesDB
from ..Models.UsersPermissionRulesModel import UsersPermissionRulesModel
from ..CommonUtils.LoggingUtil import logger
from ..CommonUtils.ConstantUtil import AdminPermission, SellerPermission, AdminPathWhiteList, SellerPathWhiteList, BuyerPathWhiteList, AdminHomePageURL, SellerHomePageURL, BuyerHomePageURL, PermissionStatusInactive

class PermissionValidationService:
    def __init__(self):
            self.usersPermissionRulesDB = UsersPermissionRulesDB()

    def hasPermission(self, usersId: int, subjectPath: str) -> bool:
        if subjectPath == None:
            return False
        usersPermissionRulesList = self.usersPermissionRulesDB.hasPermission(usersId, subjectPath)
        if usersPermissionRulesList == None:
            return False
        userItems = [usersPermissionRules.permission_subject_path for usersPermissionRules in usersPermissionRulesList]
        logger.info("orderItems: %s", userItems)
        if subjectPath not in userItems:
            return False
        return True

    def getUserPermission(self, usersId: int) -> List[UsersPermissionRulesModel]:
        return self.usersPermissionRulesDB.getPermissionByUserId(usersId)

    def hasPermissionByList(self, requestPath: str, permissionList: List[UsersPermissionRulesModel]):
        hasPermissionList = [self.hasPermission(requestPath, permission) for permission in permissionList]
        return any(hasPermissionList)

    def hasPermission(self, requestPath: str, permission: UsersPermissionRulesModel):
        if AdminPermission == permission.permission_subject_path:
            if requestPath is not None:
                matchRequestPath = [requestPath == adminPathWhite or requestPath.startswith(adminPathWhite) for adminPathWhite in AdminPathWhiteList]
                logger.info("matchRequestPath: %s, any: %s", matchRequestPath, any(matchRequestPath))
                return any(matchRequestPath)
            else:
                #if permission_status is inactive then return false
                if permission.permission_status == PermissionStatusInactive:
                    return False
                else:
                    return AdminHomePageURL
        elif SellerPermission == permission.permission_subject_path:
            if requestPath is not None:
                matchRequestPath = [requestPath == sellerPathWhite or requestPath.startswith(sellerPathWhite) for sellerPathWhite in SellerPathWhiteList]
                logger.info("matchRequestPath: %s, any: %s", matchRequestPath, any(matchRequestPath))
                return any(matchRequestPath)
            else:
                #if permission_status is inactive then return false
                if permission.permission_status == PermissionStatusInactive:
                    return False
                else:
                    return SellerHomePageURL
        else:
            if requestPath is not None:
                logger.info("buyerPathWhite: %s", requestPath)
                matchRequestPath = [requestPath == buyerPathWhite or requestPath.startswith(buyerPathWhite) for buyerPathWhite in BuyerPathWhiteList]
                logger.info("matchRequestPath: %s, any: %s", matchRequestPath, any(matchRequestPath))
                return any(matchRequestPath)
            else:
                #if permission_status is inactive then return false
                if permission.permission_status == PermissionStatusInactive:
                    return False
                else:
                    return BuyerHomePageURL