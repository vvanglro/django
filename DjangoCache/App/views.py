import random
import time
from io import BytesIO
from time import sleep

# from django.core.cache import cache
from PIL import Image, ImageFont
from PIL.ImageDraw import Draw, ImageDraw
from django.core.cache import caches
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from App.models import Student
from App.utils import get_color, generate_verification_code
from DjangoCache import settings


def index(request):
    return HttpResponse("index")


# django自带的数据库缓存
# 使用django自带的装饰器直接实现缓存
# @cache_page(30)
def news(request):

    #自己实现缓存 先获取缓存 如果没有就去查  查到后存入缓存并返回

    #这里是选择用redis做缓存  'redis_backend'这个名字就是setting里自己配置的名字
    cache = caches['redis_backend']

    result = cache.get("news")
    if result:
        return HttpResponse(result)

    news_list = []
    for i in  range(10):
        news_list.append("最近国内疫情好了很多%d" % i)
    sleep(5)
    data = {
        'news_list' : news_list
    }

    response = render(request, 'news.html', context=data)

    # 存入缓存时要key value timeout   这里的news就是key  response.content就是value将响应的内容存入
    cache.set("news", response.content, timeout=60)
    return response


# 60代表缓存60秒  cache='default'代表选择哪个库进行缓存
@cache_page(60, cache='default')
def jokes(request):

    sleep(5)

    return HttpResponse("JokeList")


def home(request):
    return HttpResponse("Home")


def get_phone(request):

    if random.randrange(100) > 95:
        return HttpResponse("恭喜你已经抢到手机")
    return HttpResponse("正在排队")


def get_ticket(request):

    return HttpResponse("还剩余99张满100减99的优惠券")


def search(request):
    return HttpResponse("这是你搜索到的种子资源")


def calc(request):

    a = 1
    b = 1
    result = (a + b)/0

    return HttpResponse(result)


#免除csrf验证的装饰器 如果模板的html里没加csrf 加装饰器也可以
@csrf_exempt
def login(request):
    if request.method == 'GET':
        global start_time
        start_time = time.time()
        # print(start_time)
        return render(request, 'login.html')
    elif request.method == 'POST':
        end_time = time.time()
        # print(end_time)
        receive_code = request.POST.get('verify_code')
        store_code = request.session.get('verifycode')
        # 将所有Session失效日期小于当前日期的数据删除，将过期的删除
        request.session.clear_expired()
        if end_time - start_time > 20:
            return HttpResponse("验证码超时")
        if receive_code.lower() != store_code.lower():
            return redirect(reverse('app:login'))
        return HttpResponse("登录成功")




def add_students(request):

    for i in range(100):
        student = Student()
        student.s_name = '小明 %d' % i
        student.s_age = i
        student.save()

    return HttpResponse("学生创建成功")


def get_students(request):
    # 自己手动实现分页
    page = int(request.GET.get('page',1))
    per_page = int(request.GET.get('per_page', 10))

    students = Student.objects.all()[per_page*(page-1): page*per_page]

    data = {
        'students': students
    }
    return render(request, 'studentlist.html', context=locals())


def get_studnets_with_page(request):


    try:
        page = int(request.GET.get('page', 1))
        # 每页多少条数据
        per_page = int(request.GET.get('per_page', 10))
        students = Student.objects.all().order_by('id')
        # django的分页
        paginator = Paginator(students, per_page)
        page_object = paginator.page(page)

        # 页数范围 paginator.page_range
        data = {
            'page_object': page_object,
            'page_range': paginator.page_range
        }
        return render(request, 'students_with_page.html', context=data)
    except Exception as e:
        print(e)
        return HttpResponse("请输入正确的数值")


def get_code(request):

    mode = 'RGB'

    size = (200, 100)

    red = get_color()
    green = get_color()
    blue = get_color()
    # 随机画布的背景颜色
    color_bg = (red, green, blue)
    # 构造画布
    image = Image.new(mode=mode, size=size, color=color_bg)
    # 初始化画笔
    imagedraw =ImageDraw(image, mode=mode)
    # 设置字体和字体大小
    imagefont = ImageFont.truetype(settings.FONT_PATH, 100)

    verify_code = generate_verification_code()
    # 通过session记录这个验证码并且设置过期时间为60秒
    request.session['verifycode'] = verify_code
    request.session.set_expiry(20)
    # 随机每个验证码的颜色
    for i in range(4):
        # 随机颜色
        fill = (get_color(),get_color(),get_color())
        imagedraw.text(xy=(50*i, 0), text=verify_code[i], font=imagefont,fill=fill)
    # 生成验证码图片上的干扰点
    for i in range(1000):
        # 随机颜色
        fill = (get_color(), get_color(), get_color())
        # xy的随机坐标和画布的大小size一样 也就是画布整体都加干扰点
        xy = (random.randrange(201),random.randrange(100))
        imagedraw.point(xy=xy, fill=fill)

    # 生成验证码图片上的干扰线
    for i in range(5):
        # 随机颜色
        fill = (get_color(), get_color(), get_color())
        # xy的随机坐标和画布的大小size一样 也就是画布整体都加干扰点
        x1 = (random.randrange(200))
        x2 = (random.randrange(200))
        y1 = (random.randrange(100))
        y2 = (random.randrange(100))
        imagedraw.line(xy=(x1,y1,x2,y2),fill=fill,width=2)
    # 内存流
    fp = BytesIO()
    # 将验证码图片存在内存流中
    image.save(fp, 'png')

    return HttpResponse(fp.getvalue(), content_type='image/png')



