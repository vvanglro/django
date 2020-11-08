import hashlib
import random
import time

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse

from Two.models import Student


def hello(request):

    return HttpResponse("Hello Two")


def login(request):
    #django中session的默认过期时间是14天  默认存在django_session表中
    #使用的base64加密  在前部添加了一个混淆串
    if request.method == "GET":
        return render(request, 'two_login.html')
    elif request.method == "POST":

        username = request.POST.get("username")

        request.session["username"] = username

        return HttpResponse("登录成功")



def mine(request):

    username = request.session.get("username")

    return render(request, 'two_mine.html', context=locals())


def logout(request):

    response = redirect(reverse('two:mine'))

    #删除session  这种删除方式会在django_session表中留下垃圾数据
    #del request.session['username']

    #删除浏览器的cookie
    #response.delete_cookie('sessionid')

    #session和cookie一起删 这种方式不会留下垃圾数据
    request.session.flush()

    return response


def register(request):

    if request.method == "GET":
        return render(request, 'student_register.html')
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            student = Student()
            student.s_name = username
            student.s_password = password
            student.save()

        except Exception as e:
            return redirect(reverse("two:register"))
        return HttpResponse("注册成功")


def student_login(request):
    if request.method == "GET":
        return render(request, 'student_login.html')
    elif request.method == "POST":
        username = request.POST.get("username")

        password = request.POST.get("password")

        students = Student.objects.filter(s_name=username).filter(s_password=password)

        if students.exists():

            student = students.first()

            ip = request.META.get("REMOTE_ADDR")

            token = generate_token(ip,username)

            student.s_token= token

            student.save()

            # response = HttpResponse("用户登录成功")
            #
            # response.set_cookie("token", token)
            #
            # return response

            data = {
                "status":200,
                "msg": "login success",
                "token": token
            }
            return JsonResponse(data=data)
        # return redirect(reverse('two:studentlogin'))

        data = {
            "status":800,
            "msg": "verify fail"
        }
        return JsonResponse(data)
def generate_token(ip, username):

    c_time = time.ctime()
    print(type(c_time))
    print(c_time)
    r = username

    return hashlib.new("md5", (ip + c_time + r).encode("utf-8")).hexdigest()


def student_mine(request):

    token = request.COOKIES.get("token")

    try:
        student = Student.objects.get(s_token=token)
    except Exception as e:
        return redirect(reverse('two:studentlogin'))

    # return HttpResponse(student.s_name)
    data = {
        "msg":"ok",
        "status":200,
        "data":{
            "username": student.s_name
        }
    }
    return JsonResponse(data=data)