from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication

from UserAuthAndPermission.models import User

# 用户登录验证
class UserAuth(BaseAuthentication):
    def authenticate(self, request):
        request_method_list = ['GET', 'PUT', 'PATCH', 'DELETE']
        if request.method in request_method_list:

            token = request.query_params.get('token')

            try:
                u_id = cache.get(token)
                user = User.objects.get(pk=u_id)

                return user, token
            except:
                return