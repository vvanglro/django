from django.conf.urls import url

from Two import views

urlpatterns = [
    url(r'^hello/', views.hello, name='hello'),
    url(r'^addperson/', views.add_person, name='add_person'),
    url(r'^addidcard/', views.add_idcard, name='add_id_card'),
    url(r'^bindcard/', views.bind_card, name='bind_card'),
    url(r'^removeperson/', views.remove_person, name='remove_person'),
    url(r'^removeidcard/', views.remove_idcard, name='remove_idcard'),
    url(r'^getperson/', views.get_person, name='get_person'),
    url(r'^getidcard/', views.get_idcard, name='get_idcard'),

    url(r'^addcustomer/', views.add_customer, name='add_customer'),
    url(r'^addgoods/', views.add_goods, name='add_goods'),
    url(r'^addtocart/', views.add_to_cart, name='add_to_cart'),
    url(r'^getgoodslist/(?P<customerid>\d+)/', views.get_goods_list, name='get_goods_list'),

    url(r'^addcat/', views.add_cat, name='add_cat'),
    url(r'^adddog/', views.add_dog, name='add_dog'),
]