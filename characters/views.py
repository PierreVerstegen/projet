from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from characters.serializer import NPCSerializer, PlayerSerializer, AttributeSerializer, AbilitiesSerializer, EffectSerializer
#comment utiliser cet élément du diable ?? Il faut que je manipule les roles en amont

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