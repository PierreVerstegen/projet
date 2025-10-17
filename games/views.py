from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import action, permission_classes
from games.serializers import GameSerializer

from .models import Game

class GameViewset(viewsets.ModelViewSet) :
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(game_master_id=self.request.user)