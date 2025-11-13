
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework import viewsets, status
from rest_framework.response import Response

from characters.serializer import BrigandyneAttributeSerializer, NPCSerializer, PlayerSerializer, AttributeSerializer, AbilitiesSerializer, EffectSerializer, BrigandyneCreateSerializer
from .models import Character, NPC, Player, Attribute, Abilities, Effect



class NPCViewset(viewsets.ModelViewSet) :
    queryset = NPC.objects.all()
    serializer_class = NPCSerializer
    permission_classes = [IsAuthenticated] # ===> ici il va falloir restreindre au role 'MJ' !!!

    def perform_create(self, serializer): #you actually need to overwrite this method to effectively link one 
        # created instance to a user ; it uses the JWT token to get 'user_id' ;
        # the method assigns the value from the token to the right cell in the table
        # Set user_id to the authenticated user's ID
        serializer.save(user_id=self.request.user)

class PlayerViewset(viewsets.ModelViewSet) :
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

# en fait il va falloir faire des views pour chaque modèle de personnage parce que nous utilisons des serializers custom 
# pour chaque modèle.

# views.py
class BrigandyneCharacterViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = BrigandyneCreateSerializer(
            data=request.data,
            context={'user': request.user}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 1. Créer le Player
        player = Player(
            charac_name=data['charac_name'],
            charac_class=data['charac_class'],
            charac_lvl=data.get('charac_lvl', 1),
            charac_money=data.get('charac_money', 0),
            charac_bio=data.get('charac_bio', ''),
            charac_model='BRIG',
            user_id=request.user,
            experience_points=0
        )
        player.save()

        # 2. Créer l'Attribute
        attribute = Attribute.objects.create(player=player) # this links Players to Attribute
        brig_data = serializer.save_to_attribute(attribute)
        # 3. Sauvegarder les stats Brigandyne
        attribute.save()
        

        # 4. Lier les abilities
        if 'abilities' in data:
            ability_objs = Abilities.objects.filter(
                ability_name__in=data['abilities'],
                ability_source='BRIG'
            )
            player.abilities.add(*ability_objs)

        # 5. Réponse
        return Response({
            'player_id': player.id,
            'attribute_id': attribute.id,
            'character': {
                'name': player.charac_name,
                'class': player.charac_class,
                'level': player.charac_lvl,
                'stats': attribute.model_brig,
                'abilities': [a.ability_name for a in player.abilities.filter(ability_source='BRIG')]
            }
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        player = get_object_or_404(Player, id=pk, charac_model='BRIG')
        attribute = getattr(player, 'attribute', None)

        return Response({
            'player_id': player.id,
            'character': {
                'name': player.charac_name,
                'stats': attribute.model_brig if attribute else {},
                'abilities': [a.ability_name for a in player.abilities.all()]
            }
        })

    def list(self, request):
        players = Player.objects.filter(charac_model='BRIG')
        data = []
        for p in players:
            attribute = getattr(p, 'attribute', None)
            data.append({
                'player_id': p.id,
                'character': {
                    'name': p.charac_name,
                    'stats': attribute.model_brig if attribute else {},
                    'abilities': [a.ability_name for a in p.abilities.all()]
                }
            })
        return Response(data)

class AttributeViewset(viewsets.ModelViewSet) :
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [IsAuthenticated]

class AbilitiesViewset(viewsets.ModelViewSet) :
    queryset = Abilities.objects.all()
    serializer_class = AbilitiesSerializer
    permission_classes = [IsAuthenticated]

class EffectViewset(viewsets.ModelViewSet) :
    queryset = Effect.objects.all()
    serializer_class = EffectSerializer
    permission_classes = [IsAuthenticated]