from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^index/', views.index, name='index'),

    url(r'^uploadfile/', views.uploadfile, name='upload_file'),

    url(r'^imagefield/', views.image_field, name='image_field'),

    url(r'^mine/', views.mine, name='mine'),
]