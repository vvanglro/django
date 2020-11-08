from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from drf.models import Book
from drf.serializers import UserSerializer, GroupSerializer, BookSerializer




class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()

    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):

    queryset = Group.objects.all()

    serializer_class = GroupSerializer

class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()

    serializer_class = BookSerializer