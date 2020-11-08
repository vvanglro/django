from django.http import HttpResponse
from django.shortcuts import render
from Two.models import Student
import random


def index(request):
    return HttpResponse('two index')


def add_student(request):

    student = Student()
    student.s_name = 'Jerry%d' % random.randrange(100)
    student.save()

    return HttpResponse('添加成功:%s' % student.s_name)


def get_students(request):

    students = Student.objects.all()

    for student in students:
        print(student.s_name)
    # return HttpResponse('获取学生列表成功')
    context = {
        "hobby" : "play games",
        "students" : students
    }
    return render(request, 'student_list.html', context=context )


def update_student(request):

    student = Student.objects.get(pk=1)
    student.s_name = 'Jack'
    student.save()
    return HttpResponse('学生信息更新成功')


def delete_student(request):

    student = Student.objects.get(pk=3)
    student.delete()
    return HttpResponse('删除学生信息成功')