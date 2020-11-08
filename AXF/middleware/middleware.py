from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from App.models import AXFUser

REQUIRE_LOGIN_JSON = [
    '/axf/addtocart/',
    '/axf/changecartstate/',
    '/axf/allselect/',
    '/axf/addshopping/',
    '/axf/subshopping/',
    '/axf/makeorder/',
]

REQUIRE_LOGIN = [
    '/axf/cart/',
    '/axf/orderdetail/',
    '/axf/orderlistnotpay/',
]


class LoginMiddleware(MiddlewareMixin):
    # 判断在闪购页面发送添加商品时 用户是否登录   没有登录返回302给前端 前端根据状态码跳转到登录页面
    # 这里因为是闪购页面内的点击事件 所以return不能直接返回跳转页面 ajax不知道 跳转页面是浏览器知道的事
    def process_request(self, request):

        if request.path in REQUIRE_LOGIN_JSON:
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    # 将用户设置到请求属性中
                    request.user = user
                except:
                    data = {
                        'status': 302,
                        'msg': 'user not avaliable'
                    }
                    return JsonResponse(data=data)
            else:
                data = {
                    'status': 302,
                    'msg': 'user not login'
                }
                return JsonResponse(data=data)

        # 这里是判断进入购物车页面时 是否有登录 没登录则可以直接跳转页面
        if request.path in REQUIRE_LOGIN:
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = AXFUser.objects.get(pk=user_id)
                    # 将用户设置到请求属性中
                    request.user = user
                except:
                    return redirect(reverse('axf:login'))
            else:
                return redirect(reverse('axf:login'))
