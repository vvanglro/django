from django.db import models


class UserModel(models.Model):

    u_name = models.CharField(max_length=16, unique=True)
    u_password = models.CharField(max_length=256)


class Address(models.Model):

    a_address = models.CharField(max_length=128)

    # related_name='address_list' 将用户获取地址时的隐性属性名改为address_list 不写的话默认address_set  也就是1获取多时的隐性属性名字改了
    a_user = models.ForeignKey(UserModel, related_name='address_list', null=True, blank=True)