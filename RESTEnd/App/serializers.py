from rest_framework import serializers

from App.models import UserModel, Address


class AddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Address
        fields = ('url', 'id', 'a_address')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    # 用户查询时 将用户对应的地址也返回  address_set名字为隐性属性 就是1对多 1获取多时用隐形属性 address_set
    # address_set = AddressSerializer(many=True, read_only=True)

    # 在模型里设置了隐形属性的名字related_name='address_list' 将用户获取地址时的隐性属性名改为address_list 不写的话默认address_set  也就是1获取多时的隐性属性名字改了
    # 所以这里可以使用自定义的名字了
    address_list = AddressSerializer(many=True, read_only=True)

    # write_only=True表明该字段仅用于反序列化输入 也就是response里不返回该字段了
    u_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ('url', 'id', 'u_name', 'u_password', 'address_list')

    # 在接口返回数据时，如果数据库表中查询出来的某些字段为null时，在前端需要多处理一些数据异常的情况。
    # django可以自定义序列化返回处理，将返回的内容限制和预处理再返回到前端。
    # 如果address_list没有数据 则不返回
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['address_list']:
            del data['address_list']
        return data
