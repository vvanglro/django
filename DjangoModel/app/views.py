import random

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from app.models import Person


def add_persons(request):

    for i in range(15):
        person = Person()
        flag = random.randrange(100)
        person.p_name = "Tom%d" % i
        person.p_age = flag
        person.p_sex = flag % 2
        person.save()

    return HttpResponse("批量创建成功")


def get_persons(request):
    #筛选满足年龄大于18,小于50的, gt代表大于 lt代表小于
    #persons = Person.objects.filter(p_age__gt=18).filter(p_age__lt=50)

    #筛选将年龄小于50的踢出去的结果并在结果中筛选出小于80的
    #persons = Person.objects.exclude(p_age__lt=50).filter(p_age__lt=80)

    #可以在上边筛选的结果上在进行筛选  in代表等于
    #persons_two = persons.filter(p_age__in=[63,64,66])

    #查询出所有的学生信息,并排序 -id 代表根据表id从大到小 不加-就是从小到大
    persons = Person.objects.all().order_by("-p_age")

    # .values可以查看queryset里字典的数据
    persons_values = persons.values()

    print(type(persons_values))

    print(persons_values)

    for person_value in persons_values:
        print(person_value)

    context = {
        'persons':persons,
    }
    return render(request, 'person_list.html', context=context)

def add_person(request):

    #person = Person.objects.create(p_name="Sunck", p_age=15, p_sex=True)

    person = Person.create('Rose')
    person.save()

    return HttpResponse("创建成功")


def get_person(request):

    #使用get查询时 1.如果没有找到符合条件的对象会引发模型类DoesNotExist异常 2.如果找到多个,会引发模型类MultipleObjectsReturned异常
    # person = Person.objects.get(p_age=100)
    # print(person)

    #返回查询集中的第一个对象
    person = Person.objects.all().first()
    print(person.p_name)

    #返回查询集中的最后一个对象
    person = Person.objects.all().last()
    print(person.p_name)

    return HttpResponse("获取成功")