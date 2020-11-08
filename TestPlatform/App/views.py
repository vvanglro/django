from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from App.models import Case, Module
from App.utils import run_main
import json

def hello(request):
    return HttpResponse("Hello")


def addcase(request):

    if request.method == 'GET':
        m_name = Module.objects.all().order_by('id')
        return render(request, 'addcase.html', context=locals())
    elif request.method == 'POST':
        m_name = request.POST.get('模块')


        c_name = request.POST.get('用例名称')
        c_method = request.POST.get('调用方式')
        c_url = request.POST.get('url')
        c_header = request.POST.get("请求头")
        c_data = request.POST.get('请求数据')
        c_code = request.POST.get('返回状态码')
        c_result = request.POST.get('期望结果')

        case = Case()
        case.c_name = c_name
        case.c_method = c_method
        case.c_url = c_url
        case.c_header = c_header
        case.c_data = c_data
        case.c_code = c_code
        case.c_result = c_result
        c_module_id = Module.objects.filter(m_name=m_name)
        # print(c_module_id.values())
        case.c_module_id = c_module_id[0].id
        case.save()

        return HttpResponse("添加成功")





def module(request):

    modules = Module.objects.all().order_by('id')

    return render(request, 'module_case_library.html', context=locals())

def get_cases(request,m_id):
    if request.method == 'GET':
        case_list = Case.objects.filter(c_module_id=m_id)
        return render(request, 'cases_list.html', context=locals())


def run_case(request,c_id):

    case = Case.objects.get(pk=c_id)
    url = case.c_url
    method = case.c_method
    data = case.c_data
    header = case.c_header
    include_result = case.c_result
    # print(url,method,data,header)
    result = run_main(url=url,method=method, data=eval(data), header=eval(header))
    # print(include_result)
    # print(result)
    if include_result in result:
        data = {
            '返回结果': result,
            '是否通过': 'Pass',
        }
        return JsonResponse(data)
    else:
        data = {
            '返回结果':result,
            '是否通过': 'Fail',
        }
        return JsonResponse(data)
