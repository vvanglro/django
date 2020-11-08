import uuid

from alipay import AliPay
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from AXF.settings import MEDIA_KEY_PREFIX, APP_PRIVATE_KEY, ALIPAY_PUBLIC_KEY, ALIPAY_APPID
from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, AXFUser, Cart, Order, \
    OrderGoods
from App.views_config import ALL_TYPE, ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN, \
    HTTP_USER_EXIST, HTTP_OK, ORDER_STATUS_NOT_PAY, ORDER_STATUS_NOT_SEND, ORDER_STATUS_NOT_RECEIVE

import pdb

from App.views_helper import hash_str, send_email_activate, get_total_price, get_pay_total_price
from celery_execute_task.sendmail import send_email_activate_celery


def home(request):
    main_wheels = MainWheel.objects.all()

    main_navs = MainNav.objects.all()

    main_mustbuys = MainMustBuy.objects.all()

    main_shops = MainShop.objects.all()

    main_shop0_1 = main_shops[0:1]
    main_shop1_3 = main_shops[1:3]
    main_shop3_7 = main_shops[3:7]
    main_shop7_11 = main_shops[7:11]

    main_shows = MainShow.objects.all()

    data = {
        'title': '首页',
        'main_wheels': main_wheels,
        'main_navs': main_navs,
        'main_mustbuys': main_mustbuys,
        'main_shop0_1': main_shop0_1,
        'main_shop1_3': main_shop1_3,
        'main_shop3_7': main_shop3_7,
        'main_shop7_11': main_shop7_11,
        'main_shows': main_shows,
    }

    return render(request, 'main/home.html', context=data)


def market(request):
    return redirect(reverse('axf:market_with_params', kwargs={
        "typeid": 104749,
        "childcid": 0,
        "order_rule": 0,
    }))


def market_with_params(request, typeid, childcid, order_rule):
    foodtypes = FoodType.objects.all()

    goodslist = Goods.objects.filter(categoryid=typeid)

    if childcid == ALL_TYPE:
        pass
    else:
        goodslist = goodslist.filter(childcid=childcid)

    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == ORDER_PRICE_UP:
        goodslist = goodslist.order_by("price")
    elif order_rule == ORDER_PRICE_DOWN:
        goodslist = goodslist.order_by("-price")
    elif order_rule == ORDER_SALE_UP:
        goodslist = goodslist.order_by("productnum")
    elif order_rule == ORDER_SALE_DOWN:
        goodslist = goodslist.order_by("-productnum")

    foodtype = foodtypes.get(typeid=typeid)
    """
        全部分类:0#进口水果:103534#国产水果:103533
        切割 #
            ['全部分类:0', '进口水果:103534', '国产水果:103533']
        切割 :
            [[全部分类,0], [进口水果,103534], [国产水果,103533]]
    """
    foodtypechildnames = foodtype.childtypenames

    foodtypechildname_list = foodtypechildnames.split("#")

    # 列表生成式
    foodtype_childname_list = [foodtypechildname.split(":") for foodtypechildname in foodtypechildname_list]

    # print(foodtype_childname_list)

    # 普通的循环处理方式
    # for foodtypechildname in foodtypechildname_list:
    #     foodtype_childname_list.append(foodtypechildname.split(":"))

    order_rule_list = [
        ['综合排序', ORDER_TOTAL],
        ['价格升序', ORDER_PRICE_UP],
        ['价格降序', ORDER_PRICE_DOWN],
        ['销量升序', ORDER_SALE_UP],
        ['销量降序', ORDER_SALE_DOWN],
    ]

    data = {
        "title": "闪购",
        "foodtypes": foodtypes,
        "goodslist": goodslist,
        "typeid": int(typeid),
        "foodtype_childname_list": foodtype_childname_list,
        'childcid': childcid,
        'order_rule_list': order_rule_list,
        'order_rule_view': order_rule,
    }

    return render(request, 'main/market.html', context=data)


def cart(request):
    carts = Cart.objects.filter(c_user=request.user)

    # 如果有商品是未选状态那就是返回False(not后变成false) 前端全选按钮就是未勾选的 否则就是勾选状态
    # 如果carts.filter(c_is_select=False)能查出来状态为false的  再exists下就是true 前边的not下 最后就是false
    # 如果carts.filter(c_is_select=False)查不出来状态为false的  再exists下就是false 前边的not下 最后就是true
    is_all_select = not carts.filter(c_is_select=False).exists()
    # print(is_all_select)

    data = {
        'title': '购物车',
        'carts': carts,
        'is_all_select': is_all_select,
        'total_price': get_total_price(user=request.user),
    }

    return render(request, 'main/cart.html', context=data)


def mine(request):
    user_id = request.session.get('user_id')
    # 1.django自动获取浏览器随机字符串取django session表里面比对
    # 2.如果比对成功 会将当前随机字符串对应的数据赋值给request.session
    # 3.通过request.session操作该数据(数据不存在也不会影响我们的业务逻辑)

    data = {
        'title': '我的',
        'is_login': False
    }
    if user_id:
        user = AXFUser.objects.get(pk=user_id)
        data['is_login'] = True
        data['username'] = user.u_username
        # 从数据库中读取图片存的路径时记得加.url  并拼接完整的地址
        data['icon'] = MEDIA_KEY_PREFIX + user.u_icon.url
        data['ORDER_STATUS_NOT_PAY'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_PAY).count()
        # data['ORDER_STATUS_NOT_SEND'] = Order.objects.filter(o_user=user).filter(o_status=ORDER_STATUS_NOT_SEND)
        data['ORDER_STATUS_NOT_RECEIVE'] = Order.objects.filter(o_user=user).filter(
            o_status__in=[ORDER_STATUS_NOT_RECEIVE, ORDER_STATUS_NOT_SEND]).count()

    return render(request, 'main/mine.html', context=data)


def register(request):
    if request.method == 'GET':

        data = {
            'title': "注册",
        }

        return render(request, 'user/register.html', context=data)

    elif request.method == 'POST':
        # pdb.set_trace()
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        icon = request.FILES.get("icon")

        # 自己写的密码加密
        # password = hash_str(password)

        # django自带的加密密码
        password = make_password(password)

        user = AXFUser()
        user.u_username = username
        user.u_password = password
        user.u_email = email
        user.u_icon = icon

        user.save()

        # .hex将uuid的格式变成字符串
        u_token = uuid.uuid4().hex

        # 将用户的id做为缓存的值 在激活的时候用id去看是哪个用户 然后并激活
        cache.set(u_token, user.id, timeout=60 * 60 * 24)

        send_email_activate_celery.delay(username=username, receive=email, u_token=u_token)

        return redirect(reverse('axf:login'))


def login(request):
    if request.method == "GET":

        error_msg = request.session.get('error_msg')

        data = {
            'title': '登录',
        }

        if error_msg:
            del request.session['error_msg']
            data['error_msg'] = error_msg

        return render(request, 'user/login.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        users = AXFUser.objects.filter(u_username=username)
        # print(users)
        # print(type(users))
        # print(users.values())
        if users.exists():
            user = users.first()
            # print(type(user))

            # django自带的验证加密密码函数 和上边的make_password对应
            if check_password(password, user.u_password):
                if user.is_active:
                    request.session['user_id'] = user.id
                    # 如果用户是第一次登录的话 需要先保存 在获取key才行
                    request.session.save()
                    print(request.session.session_key)
                    # 这句话完成了下面三件事情
                    # 1.根据当前用户生成一个随机的字符串
                    # 2.在django session表中存储该随机字符串与数据的记录
                    # 3.将随机的字符串发送给客户端浏览器

                    return redirect(reverse('axf:mine'))
                else:
                    print('用户未激活')
                    request.session['error_msg'] = '用户未激活'
                    return redirect(reverse('axf:login'))
            else:
                print('密码错误')
                request.session['error_msg'] = '密码错误'
                return redirect(reverse('axf:login'))
        print('用户不存在')
        request.session['error_msg'] = '用户不存在'
        return redirect(reverse('axf:login'))


def check_user(request):
    username = request.GET.get('username')

    users = AXFUser.objects.filter(u_username=username)

    data = {
        'status': HTTP_OK,
        'msg': 'user can use'
    }

    if users.exists():
        data['status'] = HTTP_USER_EXIST
        data['msg'] = 'user already exist'
    else:
        pass
    return JsonResponse(data=data)


def check_email(request):
    email = request.GET.get('email')

    emails = AXFUser.objects.filter(u_email=email)

    data = {
        'status': HTTP_OK,
        'msg': 'email can use'
    }

    if emails.exists():
        data['status'] = HTTP_USER_EXIST
        data['msg'] = 'email already exist'
    else:
        pass

    return JsonResponse(data=data)


def logout(request):
    request.session.flush()
    return redirect(reverse('axf:mine'))


def activate(request):
    """
    根据注册时u_token取出对应的用户id 并将用户改成已激活
    """
    u_token = request.GET.get('u_token')

    user_id = cache.get(u_token)

    if user_id:

        user = AXFUser.objects.get(pk=user_id)
        if not user.is_active:
            user.is_active = True

            user.save()

            # 用户激活后删掉redis里的缓存 这里我自己做了判断了 所以没必要删了 等缓存自己过期就好
            # cache.delete(u_token)

            return redirect(reverse('axf:login'))
        else:
            return HttpResponse("您已激活,无需再次激活")

    return render(request, 'user/activate_fail.html')


def re_activate(request):
    username = request.POST.get('username')

    user = AXFUser.objects.get(u_username=username)

    if user:

        # .hex将uuid的格式变成字符串
        u_token = uuid.uuid4().hex

        # 将用户的id做为缓存的值 在激活的时候用id去看是哪个用户 然后并激活
        cache.set(u_token, user.id, timeout=60 * 60 * 24)

        send_email_activate(username=username, receive=user.u_email, u_token=u_token)

        return HttpResponse('邮件已发送,请注意查收并再次激活')
    else:
        return HttpResponse('用户不存在')


def add_to_cart(request):
    # 获取前端传来的商品id
    goodsid = request.GET.get('goodsid')

    # 去购物车表里查看请求的用户 在筛选出当前添加的goodsid
    carts = Cart.objects.filter(c_user=request.user).filter(c_goods_id=goodsid)
    # print(carts)
    # print(type(carts))
    # print(carts.values())
    # 判断上一步筛选出来是否有数据  如果有取出来(上一步的筛选只能筛出一条数据) 并且将数量加1
    if carts.exists():
        cart_obj = carts.first()
        cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    # 如果筛选出来没有数据 则把这条数据添加到购物车表  因为模型中c_goods_num默认是1 c_is_select默认是选中 所以这里存的时候不写也可以
    else:
        cart_obj = Cart()
        cart_obj.c_goods_id = goodsid
        cart_obj.c_user = request.user

    cart_obj.save()

    # print(request.user)
    data = {
        'status': 200,
        'msg': 'add success',
        'c_goods_num': cart_obj.c_goods_num
    }
    return JsonResponse(data=data)


def change_cart_state(request):
    cart_id = request.GET.get('cartid')

    cart_obj = Cart.objects.get(pk=cart_id)

    # 这种写法改变购物车商品的选中状态 就不用写if判断了
    cart_obj.c_is_select = not cart_obj.c_is_select

    cart_obj.save()

    # 查出用户的购物车商品是否全部是勾选状态 如果有未勾选状态就返回false 如果商品都勾选状态则返回true
    is_all_select = not Cart.objects.filter(c_user=request.user).filter(c_is_select=False).exists()

    data = {
        'status': 200,
        'msg': 'change ok',
        'c_is_select': cart_obj.c_is_select,
        'is_all_select': is_all_select,
        'total_price': get_total_price(user=request.user),
    }

    return JsonResponse(data=data)


def sub_shopping(request):
    cartid = request.GET.get('cartid')

    cart_obj = Cart.objects.get(pk=cartid)

    data = {
        'status': 200,
        'msg': '减少商品数量',
    }

    if cart_obj.c_goods_num > 1:
        cart_obj.c_goods_num = cart_obj.c_goods_num - 1
        cart_obj.save()
        data['c_goods_num'] = cart_obj.c_goods_num
        data['total_price'] = get_total_price(user=request.user)
    else:
        cart_obj.delete()
        data['c_goods_num'] = 0
        data['total_price'] = get_total_price(user=request.user)

    return JsonResponse(data=data)


def add_shopping(request):
    cartid = request.GET.get('cartid')

    cart_obj = Cart.objects.get(pk=cartid)

    data = {
        'status': 200,
        'msg': '增加商品数量',
    }

    cart_obj.c_goods_num = cart_obj.c_goods_num + 1
    cart_obj.save()
    data['c_goods_num'] = cart_obj.c_goods_num
    data['total_price'] = get_total_price(user=request.user)
    return JsonResponse(data)


def all_select(request):
    cart_list = request.GET.get('cart_list')

    cart_list = cart_list.split("#")

    # 这种id__in方法可以一次性从数据库中取出列表里的所有数据
    carts = Cart.objects.filter(id__in=cart_list)

    # 然后再循环出每条数据
    for cart_obj in carts:
        # 如果是选中True状态就变成未选中False
        # 如果是未选中False状态就变成选中True
        cart_obj.c_is_select = not cart_obj.c_is_select
        cart_obj.save()

    data = {
        'status': 200,
        'msg': 'ok',
        'total_price': get_total_price(user=request.user),
    }
    return JsonResponse(data=data)


def make_order(request):
    carts = Cart.objects.filter(c_user=request.user).filter(c_is_select=True)

    order = Order()

    order.o_user = request.user

    order.o_price = get_total_price(user=request.user)

    order.save()

    for cart_obj in carts:
        ordergoods = OrderGoods()
        ordergoods.o_order = order
        ordergoods.o_goods_num = cart_obj.c_goods_num
        ordergoods.o_goods = cart_obj.c_goods
        ordergoods.o_goods_price = cart_obj.c_goods.price
        ordergoods.save()
        cart_obj.delete()

    data = {
        'status': 200,
        'msg': 'order success',
        'order_id': order.id,
    }

    return JsonResponse(data=data)


def order_detail(request):
    order_id = request.GET.get('orderid')

    order = Order.objects.get(pk=order_id)

    # 如果订单需要实时获取最新商品价格 那订单的总价也得重算一遍
    # total = get_pay_total_price(order_id)
    # order.o_price = total

    order.save()

    data = {
        'title': '订单详情',
        'order': order,
    }

    return render(request, 'order/order_detail.html', context=data)


def order_list_not_pay(request):
    orders = Order.objects.filter(o_user=request.user).filter(o_status=ORDER_STATUS_NOT_PAY)

    data = {
        'title': '订单列表',
        'orders': orders,
    }

    return render(request, 'order/order_list_not_pay.html', context=data)


def payed(request):
    order_id = request.GET.get('orderid')

    order = Order.objects.get(pk=order_id)

    order.o_status = ORDER_STATUS_NOT_SEND

    order.save()

    # 如果要实时获取最新商品价格 那订单商品表的 商品价格只能存支付时的最新商品价格
    # ordergoods = OrderGoods.objects.filter(o_order_id=order)
    # for goods in ordergoods:
    #     goods_price = Goods.objects.get(pk = goods.o_goods_id)
    #     goods.o_goods_price = goods_price.price
    #     goods.save()

    data = {
        'status': 200,
        'msg': 'payed success',
    }

    return JsonResponse(data)


def alipay(request):
    # 构建支付的客户端   AlipayClient
    alipay_client = AliPay(
        appid=ALIPAY_APPID,
        app_notify_url=None,  # 默认回调url
        app_private_key_string=APP_PRIVATE_KEY,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=ALIPAY_PUBLIC_KEY,
        sign_type="RSA",  # RSA 或者 RSA2
        debug = False  # 默认False
    )
    # 使用Alipay进行支付请求的发起

    subject = "Macbookpro 2020"

    # 电脑网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
    order_string = alipay_client.api_alipay_trade_page_pay(
        out_trade_no="111",
        total_amount=1000,
        subject=subject,
        return_url="http://www.baidu.com",
        notify_url="http://www.baidu.com"  # 可选, 不填则使用默认notify url
    )


    # 客户端操作

    return redirect("https://openapi.alipaydev.com/gateway.do?" + order_string)
