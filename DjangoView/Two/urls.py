from django.conf.urls import url

from Two import views

urlpatterns = [
    url(r'^hello/', views.hello, name='hello'),

    url(r'^login/', views.login, name='login'),

    url(r'^mine/', views.mine, name='mine'),

    url(r'^logout/', views.logout, name='logout'),

    url(r'^register/', views.register, name='register'),

    url(r'^studentlogin/', views.student_login, name='studentlogin'),

    url(r'^studentmine/', views.student_mine, name='studentmine'),
]