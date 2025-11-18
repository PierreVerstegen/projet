from django.shortcuts import get_object_or_404, render
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
    # ici on créée une méthode pour lire les données avec un id ; 
    def retrieve(self, request, pk=None):
        game = get_object_or_404(Game, id = pk)
        user = getattr(game, 'games_mastered', None) #nécessaire pour accéder aux valeurs dasn les tables liées
        players = getattr(game, 'players', None)
        npcs = getattr(game, 'npcs', None)

        return Response({
            'game_id': game.id,
            'game_name' : game.game_name,
            'game_started_on': game.game_started_on,
            'game_theme' : game.game_theme,
            'game_master' : user.user_name,
            'players' : [p.charac_name for p in players] if players else [],
            'npcs' : [n.charac_name for n in npcs] if npcs else []
        })


    def list(self, request):
        games = Game.objects.all()
        data = []
        for g in games :
            user = getattr(g, 'games_mastered', None)
            players = getattr(g, 'players', None)
            npcs = getattr(g, 'npcs', None)
            data.append({
                'game_id': g.id,
                'game_name' : g.game_name,
                'game_started_on': g.game_started_on,
                'game_theme' : g.game_theme,
                'game_rules' : g.game_model,
                'game_master' : user.user_name,
                'players' : [p.charac_name for p in players] if players else [],
                'npcs' : [n.charac_name for n in npcs] if npcs else []
            })