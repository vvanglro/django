from django.db import models


class Person(models.Model):
    p_name = models.CharField(max_length=16)
    p_sex= models.BooleanField(default=False)

class IDCard(models.Model):
    id_num= models.CharField(max_length=18, unique=True)

    #null=True表示数据库中可以为null空   blank=True表示提交的表单可以为空
    #on_delete=models.PROTECT表示删除时受保护 在删除Person表中和IDCard表中有绑定关系的person时会删不掉 如果先删除idcard 在删除person 则可删除
    #on_delete=models.SET_NULL时表示删除绑定关系的person时 idcard变空变为未绑定 设置SET_NULL时前提得允许为null
    id_person = models.OneToOneField(Person, null=True, blank=True, on_delete=models.SET_NULL)


class Customer(models.Model):

    c_name= models.CharField(max_length=16)

class Goods(models.Model):

    g_name = models.CharField(max_length=16)
    g_customer = models.ManyToManyField(Customer)

#购物车不推荐多对多 使用下边这种方式 使用外键来自己维护
# class Cart(models.Model):
#
#     customerid = models.ForeignKey(Customer)
#     goodid = models.ForeignKey(Goods)





# 模型继承
# django中模型支持继承
# 默认继承是会将通用字段放到父表中, 特定字段放在自己的表中. 中间使用外键连接
   # 关系型数据库关系越复杂, 效率越低, 查询越慢
   # 父类表中也会存储过多的数据
# 使用元信息来解决这个问题
   # 使模型抽象化
   # 抽象的模型就不会在数据库中产生映射了
   # 子模型映射出来的表直接包含父模型的字段
class Animal(models.Model):

    a_name = models.CharField(max_length=16)
    # 元信息
    class Meta:
        # 使模型抽象化
        abstract = True

class Cat(Animal):
    c_eat = models.CharField(max_length=32)


class Dog(Animal):
    d_legs = models.IntegerField(default=4)