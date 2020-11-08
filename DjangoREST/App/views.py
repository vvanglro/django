from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from App.models import Game
from App.serializers import GameSerializer


# ListCreateAPIView创建和列表查询
class GamesView(ListCreateAPIView):

    serializer_class = GameSerializer

    queryset = Game.objects.all()


# RetrieveUpdateDestroyAPIView获取单个数据 更新单个数据, 删除单个数据的类视图
class GameView(RetrieveUpdateDestroyAPIView):

    serializer_class = GameSerializer

    queryset = Game.objects.all()


# ModelViewSet继承了增删改查
class GameModelViewSet(ModelViewSet):

    serializer_class = GameSerializer

    queryset = Game.objects.all()