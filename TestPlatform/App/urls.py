from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^hello/', views.hello, name='hello'),
    url(r'^addcase/', views.addcase, name='addcase'),
    url(r'^module/', views.module, name='module'),
    url(r'^getcases/(\d+)/', views.get_cases, name='get_cases'),
    url(r'^runcase/(\d+)/', views.run_case, name='run_case'),
]