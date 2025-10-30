
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from characters.serializer import BrigandyneAttributeSerializer, NPCSerializer, PlayerSerializer, AttributeSerializer, AbilitiesSerializer, EffectSerializer, BrigandyneCreateSerializer
#comment utiliser cet élément du diable ?? Il faut que je manipule les roles en amont
from rest_framework.response import Response
from .models import Character, NPC, Player, Attribute, Abilities, Effect

from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone

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
            charac_hp=data['computed']['pv'],
            charac_money=data.get('charac_money', 0),
            charac_bio=data.get('charac_bio', ''),
            charac_model='BRIG',
            user_id=request.user,
            experience_points=0
        )
        player.save()

        # 2. Créer l'Attribute
        attribute = Attribute.objects.create()
        attribute.players.add(player)

        # 3. Sauvegarder les stats Brigandyne
        attribute.model_brig = {
            'raw': data['raw'],
            'computed': data['computed'],
            'meta': {
                'created_at': timezone.now().isoformat(),
                'created_by': request.user.id
            }
        }
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
                'hp': player.charac_hp,
                'stats': attribute.model_brig,
                'abilities': [a.ability_name for a in player.abilities.filter(ability_source='BRIG')]
            }
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        player = Player.objects.get(id=pk, charac_model='BRIG')
        attribute = player.attributes.first()
        return Response({
            'player_id': player.id,
            'character': {
                'name': player.charac_name,
                'hp': player.charac_hp,
                'stats': attribute.model_brig,
                'abilities': [a.ability_name for a in player.abilities.all()]
            }
        })

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