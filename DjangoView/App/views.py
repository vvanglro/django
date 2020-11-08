import base64
import random

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect

# Create your views here.
from django.urls import reverse


def hello(request):

    response = HttpResponse()

    # response.content = "德玛西亚"
    #
    # response.status_code = 404

    response.write("听说马桶堵了")

    response.flush()

    return response


def get_ticket(request):

    #反向解析
    url = reverse('app:hello')
    print(url)

    if random.randrange(10) > 5:
        #重定向的2种方法
        return redirect(url)
        # return HttpResponseRedirect(url)

    return HttpResponse("恭喜你抢到票了")


def get_info(request):

    data = {
        "msg":"ok",
        "status": 200
    }
    #以json格式返回数据
    return JsonResponse(data=data)


def set_cookie(request):

    response = HttpResponse("设置cookie")

    response.set_cookie('username', 'Rock')

    return response


def get_cookie(request):

    username = request.COOKIES.get("username")

    return HttpResponse(username)


def login(request):
    return render(request, 'login.html')


def dologin(request):

    uname = request.POST.get('uname')

    #因为cookie默认不支持中文, 所以在接收到输入中文时先转码存
    uname = str(base64.b64encode(uname.encode("utf-8")), "utf-8")

    #反向解析到mine
    response = HttpResponseRedirect(reverse('app:mine'))

    #max_age设置cookie过期时间  max_age=60代表1分钟后过期
    # response.set_cookie('uname', uname, max_age=60)

    response.set_signed_cookie('uname', uname, salt="Rock", max_age=10)

    return response


def mine(request):
    '''
    因为在设置cookie时使用了过期时间, 所以在获取到过期后的cookie时是None会报错
    利用python的异常捕获 当try里报错时 执行except里的
    '''
    # uname = request.COOKIES.get('uname')
    try:
        #如果cookie是加密的  在获取时使用这种方式进行解密 salt参数值同加密时的
        uname = request.get_signed_cookie('uname', salt="Rock")

        #判断cookie是否还在  如果在正常返回 如果不在则跳转到登录页面
        if uname:
            # 返回时解码反在if里边 因为cookie过期后 返回None  base解码时会报错所以反正if里边
            uname = str(base64.b64decode(uname), "utf-8")
            return render(request, 'mine.html', context={"uname": uname})
        return HttpResponseRedirect(reverse('app:login'))

    except:

        return HttpResponseRedirect(reverse('app:login'))



def logout(request):

    response = redirect(reverse('app:login'))

    #删除浏览器cookie   让浏览器把cookie变过期
    response.delete_cookie('uname')

    return response