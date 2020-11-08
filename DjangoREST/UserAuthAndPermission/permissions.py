from rest_framework.permissions import BasePermission


from UserAuthAndPermission.models import User

# 验证用户权限
class IsSuperUser(BasePermission):


    def has_permission(self, request, view):
        request_method_list = ['GET', 'PUT', 'PATCH', 'DELETE']
        if request.method in request_method_list:
            if isinstance(request.user, User):
                return request.user.is_super
            return False
        return True