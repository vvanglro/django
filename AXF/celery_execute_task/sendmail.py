import time
from django.core.mail import send_mail
from celery import Celery


# 初始化django环境
import django
import os

from django.template import loader

from AXF.settings import  SERVER_HOST, SERVER_PORT, EMAIL_FROM

# 启动命令 celery -A celery_execute_task.sendmail worker --loglevel=info -P eventlet

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AXF.settings')
django.setup()

# 创建实例对象
# 第一个parameter：可随意命名，但一般为本文件所在路径
# broker：指定中间人，斜杠后指定第几个数据库
app = Celery('celery_execute_task.sendmail', broker='redis://127.0.0.1:6379/1')


# 定义任务函数
@app.task
def send_email_activate_celery(username, receive, u_token):

    subject = '%s AXF Activate' % username

    # message = 'Hello'

    from_email = EMAIL_FROM

    recipient_list = [receive,]

    data = {
        'username': username,
        'activate_url': 'http://{}:{}/axf/activate/?u_token={}'.format(SERVER_HOST, SERVER_PORT, u_token)
    }

    # loader加载模板 并渲染成html
    html_message = loader.get_template('user/activate.html').render(data)

    send_mail(subject=subject, message='', html_message=html_message, from_email=from_email, recipient_list=recipient_list)
