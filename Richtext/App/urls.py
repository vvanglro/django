from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/', views.index),

    url(r'^editblog/', views.edit_blog, name='edit_blog'),
]