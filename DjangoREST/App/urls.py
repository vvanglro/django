from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from App import views

urlpatterns = [
    url(r'^games/$', views.GamesView.as_view()),
    url(r'^games/(?P<pk>\d+)/$', views.GameView.as_view(), name='game-detail'),

    # url(r'^game/', views.GameModelViewSet.as_view({'get': 'list'})),
]

router = DefaultRouter()
router.register(r'game', views.GameModelViewSet)
urlpatterns += router.urls