import hashlib
import time
from _pydecimal import Decimal,ROUND_HALF_UP
from django.core.mail import send_mail
from django.template import loader

from AXF.settings import EMAIL_HOST_USER, SERVER_HOST, SERVER_PORT
from App.models import Cart, Order


def hash_str(source):
    return hashlib.new('sha512', source.encode('utf-8')).hexdigest()


def send_email_activate(username, receive, u_token):

    subject = '%s AXF Activate' % username

    # message = 'Hello'

    from_email = EMAIL_HOST_USER

    recipient_list = [receive,]

    data = {
        'username': username,
        'activate_url': 'http://{}:{}/axf/activate/?u_token={}'.format(SERVER_HOST, SERVER_PORT, u_token)
    }

    # loader加载模板 并渲染成html
    html_message = loader.get_template('user/activate.html').render(data)

    send_mail(subject=subject, message='', html_message=html_message, from_email=from_email, recipient_list=recipient_list)

    time.sleep(5)

def get_total_price(user):

    carts = Cart.objects.filter(c_user=user).filter(c_is_select=True)

    total = 0

    for cart in carts:
        total += cart.c_goods_num * cart.c_goods.price

    # Decimal用于精准计算  Decimal('0.00')表示保留小数点后两位 ROUND_HALF_UP四舍五入
    total = str(Decimal(total).quantize(Decimal('0.00'),ROUND_HALF_UP))
    return total


def get_pay_total_price(orderid):

    order = Order.objects.get(pk=orderid)

    goods_list = order.ordergoods_set.all()

    total = 0
    for goods in goods_list:
        total += goods.o_goods.price * goods.o_goods_num

    total = str(Decimal(total).quantize(Decimal('0.00'), ROUND_HALF_UP))

    return total
