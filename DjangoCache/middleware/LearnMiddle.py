import random
import time

from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

# 已Mixin结尾的大部分都是基类和多继承
class HelloMiddle(MiddlewareMixin):

    def process_request(self, request):

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            print(request.META.get('HTTP_X_FORWARDED_FOR'))
        else:
            print(request.META.get('REMOTE_ADDR'))


        ip = request.META.get("REMOTE_ADDR")
        # if request.path == "/app/getphone":
        #     if ip == "127.0.0.1":
        #         if random.randrange(100) > 20 :
        #             return HttpResponse("恭喜你免费获得了手机")
        #
        #
        # if request.path == "/app/getticket/":
        #     if ip.startswith('192.168.0.13'):
        #         return HttpResponse("优惠劵已经抢光")
        #
        #
        # # 10秒之内只能搜索一次
        # if request.path == "/app/search/":
        #     # 从缓存中获取ip
        #     result = cache.get(ip)
        #     # 如果存在这个ip则返回频繁
        #     if result:
        #         return HttpResponse("您的访问过于频繁, 请10秒之后再次搜索")
        #     # 不存在则加入缓存 过期时间为10秒
        #     cache.set(ip, ip, timeout=10)


        # 反爬虫60秒之内只能访问10次 超过返回请求频繁  如果60秒只能请求超过30次则黑名单一天
        # black_list = cache.get('black', [])
        # # print(black_list)
        # if ip in black_list:
        #     return HttpResponse("黑名单用户, 凉凉")
        #
        # requests = cache.get(ip, [])
        # #print('已有的时间',requests)
        # while requests and time.time() - requests[-1] > 60:
        #     requests.pop()
        # #将每次访问的时间加到列表的第一个位置也就是列表的下标0
        # requests.insert(0, time.time())
        # #print(requests)
        # cache.set(ip, requests, timeout=60)
        #
        #
        # if len(requests) > 30:
        #     black_list.append(ip)
        #     cache.set('black', black_list, timeout=60 * 60 * 24)
        #     return HttpResponse("小爬虫小黑屋里呆一天吧")
        #
        #
        # if len(requests) > 10:
        #     return HttpResponse("请求次数过于频繁, 小爬虫回家睡觉吧")



    # 重写异常 发生500就重定向到index页面
    # def process_exception(self, request, exception):
    #     print(request, exception)
    #     return redirect(reverse('app:index'))




