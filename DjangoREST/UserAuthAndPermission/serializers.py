from rest_framework import serializers

from UserAuthAndPermission.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'id', 'u_name', 'u_password', 'is_super')