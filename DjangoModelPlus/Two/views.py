from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Two.models import Person, IDCard, Customer, Goods, Cat, Dog


def hello(request):
    return HttpResponse('Two Hello')


def add_person(request):
    username = request.GET.get("username")

    person = Person()

    person.p_name = username

    person.save()

    return HttpResponse("Person创建成功%s" % person.id)


def add_idcard(request):
    id_num = request.GET.get("idnum")

    idcard = IDCard()

    idcard.id_num = id_num

    idcard.save()

    return HttpResponse("IDCard %d" % idcard.id)


def bind_card(request):
    person = Person.objects.last()

    idcard = IDCard.objects.last()

    idcard.id_person = person

    idcard.save()

    return HttpResponse("绑定成功")


def remove_person(request):
    person = Person.objects.last()

    person.delete()

    return HttpResponse("人员移除成功")


def remove_idcard(request):
    idcard = IDCard.objects.last()

    idcard.delete()
    return HttpResponse("身份证移除成功")


def get_person(request):
    idcard = IDCard.objects.last()

    # 1对1级联数据获取
    # 从获取主, 显性属性, 就是属性的名字
    person = idcard.id_person

    return HttpResponse(person.p_name)


def get_idcard(request):
    person = Person.objects.last()

    # 1对1级联数据获取
    # 主获取从, 隐形属性, 默认就是级联模型的名字
    idcard = person.idcard

    return HttpResponse(idcard.id_num)


def add_customer(request):
    c_name = request.GET.get('cname')

    customer = Customer()

    customer.c_name = c_name

    customer.save()

    return HttpResponse("创建消费者成功 %d" % customer.id)


def add_goods(request):

    g_name = request.GET.get('gname')

    goods = Goods()

    goods.g_name = g_name

    goods.save()

    return HttpResponse("创建商品成功 %d" % goods.id)


def add_to_cart(request):

    customer = Customer.objects.last()

    goods = Goods.objects.last()

    # print(type(goods.g_customer))
    # print(goods.g_customer)

    # 多对多级联查询
    # 从获取主 使用属性 属性是一个Manager子类
    # goods.g_customer.add(customer)

    # 级联数据 add  remove clear set

    # 多对多级联查询
    # 主获取从 使用隐性属性 也是Manager子类,操作和从获取主完全一样
    customer.goods_set.add(goods)

    return HttpResponse("添加成功")


def get_goods_list(request, customerid):

    # 获取消费者id
    customer = Customer.objects.get(pk=customerid)

    # 使用级联查询 查出该消费者都买了哪些商品
    goods_list = customer.goods_set.all()

    return render(request, 'goods_list.html', context=locals())


def add_cat(request):

    cat = Cat()

    cat.a_name = "cat_name"
    cat.c_eat = "Fish"
    cat.save()
    return HttpResponse("Cat创建成功 %d" %cat.id)

def add_dog(request):

    dog = Dog()

    dog.a_name = "dog_name"
    dog.save()
    return HttpResponse("Dog创建成功 %d" %dog.id)