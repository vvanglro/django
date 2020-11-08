from django.conf.urls import url

from Two import views

urlpatterns = [
    url(r'^getuser/', views.get_user),
    url(r'^getusers/', views.get_users),
    url(r'^getorders/', views.get_orders),
    url(r'^getgrades/', views.get_grades),
    url(r'^getcustomer/', views.get_customer),
    url(r'^getcompany/', views.get_company),
    url(r'^getanimals/', views.get_animals),
]