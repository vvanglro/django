from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^addpersons/', views.add_persons),
    url(r'^getpersons/', views.get_persons),
    url(r'^addperson/', views.add_person),
    url(r'^getperson/', views.get_person),
]