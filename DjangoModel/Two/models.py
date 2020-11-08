from django.db import models

# Create your models here.

#python manage.py makemigrations
#python manage.py migrate

class User(models.Model):
    #unique :如果为True，该字段在整个表格中必须是唯一的
    u_name = models.CharField(max_length=16, unique=True)
    u_password = models.CharField(max_length=256)

class Order(models.Model):
    o_num = models.CharField(max_length=16, unique=True)
    o_time = models.DateTimeField(auto_now_add=True)

class Grade(models.Model):
    g_name = models.CharField(max_length=16)

class Student(models.Model):
    s_name = models.CharField(max_length=16)
    s_grade = models.ForeignKey(Grade)

class Customer(models.Model):
    c_name = models.CharField(max_length=16)
    c_cost = models.IntegerField(default=10)

class Company(models.Model):
    c_name= models.CharField(max_length=16)
    c_gril_num = models.IntegerField(default=5)
    c_boy_num = models.IntegerField(default=3)


#自己写manager管理类 继承models.Manager这个类 并重写这个类下的get_queryset方法
class AnimalsManager(models.Manager):

    def get_queryset(self):
        #https://www.runoob.com/python/python-func-super.html 关于super函数
        return super().get_queryset().filter(is_delete=False)

    def create_animal(self, a_name="Chicken"):
        a = self.model()
        a.a_name = a_name
        return a

class Animals(models.Model):
    a_name = models.CharField(max_length=16)
    is_delete = models.BooleanField(default=False)

    #自己重写管理者
    a_m = AnimalsManager()

    #可以自定义管理者 这样写 在查询时就是 模型类.a_m.all() 不自定义则是模型类.objects.all()
    #a_m = models.Manager()