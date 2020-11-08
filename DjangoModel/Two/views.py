from django.db.models import Max, Avg, F, Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Two.models import User, Order, Grade, Customer, Company, Animals, AnimalsManager


def get_user(request):

    username = "Sunck"
    password = "120"

    users = User.objects.filter(u_name=username)

    print(users.count())

    if users.count():
        user = users.first()

        if user.u_password == password:
            print("获取用户信息成功")
        else:
            print("密码错误")
    else:
        print("用户不存在")
    return HttpResponse("获取成功")


def get_users(request):

    #下标不能为负数
    users = User.objects.all()[0:4]

    context = {
        "users" : users
    }

    return render(request, 'user_list.html', context=context)


def get_orders(request):
    #根据月份进行查询 django有自定义的时区需要去settings中将USE_TZ = True改为False
    orders = Order.objects.filter(o_time__month=8)

    for order in orders:
        print(order.o_num)

    return HttpResponse("获取订单成功")


def get_grades(request):
    #从班级表中查询班里有叫Sunck学生的班级名
    grades = Grade.objects.filter(student__s_name='Sunck')

    for grade in grades:
        print(grade.g_name)

    return HttpResponse("获取成功")


def get_customer(request):
    #查询表中的消费并平均   有avg max min count sum
    result = Customer.objects.aggregate(Avg("c_cost"))
    print(result)
    return HttpResponse("获取花费成功")


def get_company(request):
    #从表中获取男生人数小于女生人数的公司名  lt是小于 gt是大于  用F()函数可以获取我们属性的值, 可以实现一个模型的不同属性的运算操作. 还可以支持算术运算
    #companies = Company.objects.filter(c_boy_num__lt=F('c_gril_num'))

    #从表中获取男生人数小于女生人数减完15后的公司名
    # companies = Company.objects.filter(c_boy_num__lt=F('c_gril_num')-15)

    #从表中查询出男生人数大于1并且女生人数大于10的公司名 使用Q函数可以对条件进行封装,封装之后,可以支持逻辑运算  与 & and   或 | or   非 ~ not
    # companies = Company.objects.filter(c_boy_num__gt=1).filter(c_gril_num__gt=10)
    companies = Company.objects.filter(Q(c_boy_num__gt=1) & Q(c_gril_num__gt=10))

    for company in companies:
        print(company.c_name)

    return HttpResponse("获取公司成功")


def get_animals(request):

    #在models中有重写管理者所以这里用a_m
    animals = Animals.a_m.all()

    for animal in animals:
        print(animal.a_name)

    #模型类调用重写管理者的create_animal方法
    a = Animals.a_m.create_animal("ig")
    a.save()

    return HttpResponse("获取动物成功")