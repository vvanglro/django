from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from Two.models import Grade, Student


def students(request,g_id):

    student_list = Student.objects.filter(s_grade_id=g_id).filter(is_delete=False)

    return render(request, 'grade_student_list.html', context=locals())


def student(request, s_id):

    print(s_id)

    print(type(s_id))

    return HttpResponse("Get Student Success")


def grades(request):

    grade_list = Grade.objects.all()

    #locals内置函数   将局部变量使用字典的方式进行打包   Key是变量名, value是变量中存储的数据
    return render(request, 'grade_list.html', context=locals())


def get_time(request, hour, minute, second):

    return HttpResponse("Time %s: %s: %s" %(hour,minute, second))


def get_date(request, day, month, year):

    return HttpResponse("Date %s- %s- %s"%(year, month, day))


def learn(request):
    return HttpResponse("love learn")


def get_studentpage(request,student_id):
    # student_name = Student.objects.filter(pk=student_id)
    # student_name = student_name.values('s_name')[0]['s_name']

    student_name = Student.objects.get(pk=student_id)
    #student_name = student_name.s_name
    return render(request, 'student_page.html', context=locals())


def delete_student(request, student_id):

    student = Student.objects.get(pk=student_id)
    student.is_delete = True
    student.save()
    return HttpResponse("删除成功")


def add_student(request):

    s_name = request.POST.get("学生名字")
    s_grade = request.POST.get("班级ID")
    student = Student()
    student.s_name = s_name
    student.s_grade_id = int(s_grade)
    student.save()
    return HttpResponse("新增学生成功")


def have_request(request):
    # http://127.0.0.1:8000/two/haverequest/?hobby=codong&hobby=sleeping
    print(request.path)

    print(request.method)

    print(request.GET)
    # print(request.GET["hobby"])  #使用这种情况获取时 在没传hobby时会报错

    #获取get请求中的参数
    print(request.GET.get('hobby'))
    print(request.GET.getlist('hobby'))
    print(request.POST)

    #print(request.META) #打印出用户请求的所有信息
    for key in request.META:
        print(key, request.META.get(key))
    print('REMOTE_ADDR:',request.META.get('REMOTE_ADDR')) #打印出用户的ip地址
    return HttpResponse("Request Success")


def test(request):

    students = Student.objects.all()
    for student in students:
        grade = student.s_grade
        print(grade.g_name)
    return HttpResponse("成功")