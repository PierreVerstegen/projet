from django.shortcuts import redirect, render
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import CustomUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
