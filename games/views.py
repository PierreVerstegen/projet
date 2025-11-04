from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.decorators import action, permission_classes
from games.serializers import GameSerializer
from characters.models import Player
from .models import Game
from rest_framework.response import Response

class GameViewset(viewsets.ModelViewSet) :
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(game_master_id=self.request.user)
    
    # @action(detail=False, methods=["patch"], url_path="add_player")
    # def add_player(self, serializer):
    #     serializer = PlayerUpdateSerializer
    #     serializer.partial_update(players=self.request.players)

    @action(detail=True, methods=['post'], url_path='add-players')
    def add_players(self, request, pk=None):
        game = self.get_object()
        player_ids = request.data.get('player_ids', [])
        if not player_ids:
            return Response({"error": "No player IDs provided"}, status=400)
        players = Player.objects.filter(id__in=player_ids)
        if len(players) != len(player_ids):
            return Response({"error": "One or more player IDs are invalid"}, status=400)
        game.players.add(*players)
        serializer = self.get_serializer(game)
        return Response(serializer.data)