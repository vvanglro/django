from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from App.models import User


def index(request):
    return render(request, 'index.html')


def uploadfile(request):
    # 将上传的图片直接手动保存到静态资源路径中
    if request.method == 'GET':
        return render(request, 'upload.html')
    elif request.method == 'POST':
        icon = request.FILES.get('icon')
        print(type(icon))

        with open('./static/img/icon.jpg', 'wb') as save_file:
            # chunks把文件分成小块 防止上传大文件把内存卡住
            for part in icon.chunks():
                save_file.write(part)
                save_file.flush()
        return HttpResponse("文件上传成功")


def image_field(request):
    # 保存用户名和头像 将头像路径存入数据库中 资源存放在配置的路径中

    if request.method == 'GET':
        return render(request, 'image_field.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        icon = request.FILES.get('icon')

        user = User()

        user.u_name = username
        user.u_icon = icon
        user.save()

        return HttpResponse("上传成功")


def mine(request):
    # 获取用户名和头像并显示
    username = request.GET.get('username')
    user = User.objects.get(u_name=username)

    print("/static/upload/"+user.u_icon.url)

    data = {
        'username': username,
        'icon_url' : "/static/upload/"+user.u_icon.url
    }
    return render(request, 'mine.html', context=data)