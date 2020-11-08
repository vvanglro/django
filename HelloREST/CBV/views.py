from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView

from CBV.models import Book


class HelloCBV(View):

    msg = None

    def get(self, request):
        return HttpResponse("类视图GET哈哈哈 %s" % self.msg)

    def post(self, request):
        return HttpResponse("POST 666")

    def put(self, request):
        return HttpResponse("PUT 666")


class BooksCBV(View):

    def get(self, request):
        book_list = Book.objects.all()

        book_list_json = []

        for book in book_list:
            book_list_json.append(book.to_dict())

        data = {
            'status': 200,
            'msg': 'ok',
            'data': book_list_json
        }

        return JsonResponse(data=data)

    def post(self, request):
        b_name = request.POST.get('b_name')
        b_price = request.POST.get('b_price')

        book = Book()
        book.b_name = b_name
        book.b_price = b_price
        book.save()

        data = {
            'status': 201,
            'msg': 'add success',
            'data': book.to_dict()
        }

        return JsonResponse(data=data, status=201)





class HelloView(View):

    def get(self, request):
        return render(request, 'hello.html')

class HelloTemplateView(TemplateView):

    template_name='hello.html'

class HelloListView(ListView):
    template_name = 'Booklist.html'

    model = Book