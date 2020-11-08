from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^hello/', views.hello, name='hello'),
    url(r'^getticket/', views.get_ticket, name='get_ticket'),
    url(r'^getinfo/', views.get_info, name='get_info'),
    url(r'^setcookie/', views.set_cookie, name='set_cookie'),

    url(r'^getcookie/', views.get_cookie, name='get_cookie'),
    url(r'^login/', views.login, name='login'),

    url(r'^dologin/', views.dologin, name='dologin'),

    url(r'^mine/', views.mine, name='mine'),

    url(r'^logout/', views.logout, name='logout'),
]