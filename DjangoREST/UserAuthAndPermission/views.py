import uuid

from django.core.cache import cache
from rest_framework import status, exceptions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from DjangoREST.settings import SUPER_USERS
from UserAuthAndPermission.auth import UserAuth
from UserAuthAndPermission.constants import HTTP_ACTION_REGISTER, HTTP_ACTION_LOGIN
from UserAuthAndPermission.models import User
from UserAuthAndPermission.permissions import IsSuperUser
from UserAuthAndPermission.serializers import UserSerializer


class UsersAPIView(ListCreateAPIView):
    serializer_class = UserSerializer

    queryset = User.objects.all()
    # 用户登录验证
    authentication_classes = (UserAuth,)
    # 用户权限验证
    permission_classes = (IsSuperUser,)

    # def get(self, request, *args, **kwargs):
    #     if isinstance(request.user, User):
    #         return self.list(request, *args, **kwargs)
    #     else:
    #         raise exceptions.NotAuthenticated

    def post(self, request, *args, **kwargs):
        action = request.query_params.get('action')

        if action == HTTP_ACTION_REGISTER :
            return self.create(request, *args,**kwargs)
        elif action == HTTP_ACTION_LOGIN:
            u_name = request.data.get('u_name')
            print(u_name)
            u_password = request.data.get('u_password')
            print(u_password)

            try:
                user = User.objects.get(u_name=u_name)

                if user.u_password == u_password:
                    token = uuid.uuid4().hex
                    cache.set(token, user.id)
                    data = {
                        'msg': 'login success',
                        'status': 200,
                        'token': token
                    }
                    return Response(data)
                else:
                    raise exceptions.AuthenticationFailed
            except User.DoesNotExist:
                raise exceptions.NotFound
        else:
            raise exceptions.ValidationError


    # 重写了ListCreateAPIView类里的方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        data = serializer.data
        print(data)

        u_name = data.get('u_name')
        print(u_name)

        if u_name in SUPER_USERS:
            print('创建超级用户')
            u_id = data.get('id')

            user = User.objects.get(pk=u_id)

            user.is_super = True

            user.save()
            data['is_super'] = True

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)




class UserAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    queryset = User.objects.all()

    # 用户登录验证
    authentication_classes = (UserAuth,)
    # 用户权限验证
    permission_classes = (IsSuperUser,)
    # def post(self, request, *args, **kwargs):
    #
    #     return Response({'msg':'error'},status=404)

