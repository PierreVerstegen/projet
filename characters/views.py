from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from characters.serializer import NPCSerializer, PlayerSerializer, AttributeSerializer, AbilitiesSerializer, EffectSerializer
#comment utiliser cet élément du diable ?? Il faut que je manipule les roles en amont

from .models import Character, NPC, Player, Attribute, Abilities, Effect

class NPCViewset(viewsets.ModelViewSet) :
    queryset = NPC.objects.all()
    serializer_class = NPCSerializer
    permission_classes = [IsAuthenticated] # ===> ici il va falloir restreindre au role 'MJ' !!!

class PlayerViewset(viewsets.ModelViewSet) :
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]

class AttributeViewset(viewsets.ModelViewSet) :
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    permission_classes = [IsAuthenticated]

class AbilitiesViewset(viewsets.ModelViewset) :
    queryset = Abilities.objects.all()
    serializer_class = AbilitiesSerializer
    permission_classes = [IsAuthenticated]

class EffectViewset(viewsets.ModelViewset) :
    queryset = Effect.objects.all()
    serializer_class = EffectSerializer
    permission_classes = [IsAuthenticated]