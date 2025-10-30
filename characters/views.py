from datetime import timezone
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from characters.serializer import BrigandyneAttributeSerializer, NPCSerializer, PlayerSerializer, AttributeSerializer, AbilitiesSerializer, EffectSerializer
#comment utiliser cet élément du diable ?? Il faut que je manipule les roles en amont
from rest_framework.response import Response
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
    
    def create(self, request, *args, **kwargs):
        # 1. Créer ou récupérer l'instance Attribute
        attribute_id = request.data.get('attribute_id')
        if attribute_id:
            try:
                attribute = Attribute.objects.get(id=attribute_id)
            except Attribute.DoesNotExist:
                return Response({"error": "Attribute non trouvé"}, status=404)
        else:
            attribute = Attribute()

        # 2. Valider les données
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        raw_data = serializer.validated_data

        # 3. Calculer les stats dérivées
        computed = serializer.compute_derived_stats(raw_data)

        # 4. Structurer le JSON
        brig_data = {
            'raw': {
                'combat': raw_data['combat'],
                'connaissances': raw_data['connaissances'],
                # ... tous les champs bruts
                'race': raw_data.get('race'),
                'is_important_npc': raw_data.get('is_important_npc', True),
                'archetype': raw_data.get('archetype'),
            },
            'computed': computed,
            'meta': {'updated_at': timezone.now().isoformat()}
        }

        # 5. Sauvegarder
        attribute.model_brig = brig_data
        attribute.save()

        # 6. Réponse
        return Response({
            'attribute_id': attribute.id,
            'brigandyne': brig_data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        attribute = get_object_or_404(Attribute, pk=pk)
        return Response({
            'attribute_id': attribute.id,
            'brigandyne': attribute.model_brig
        })

    def update(self, request, *args, **kwargs):
        # Même logique que create, mais on récupère l'objet existant
        attribute = self.get_object()  # ← récupère via pk

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        raw_data = serializer.validated_data

        computed = serializer.compute_derived_stats(raw_data)

        brig_data = {
            'raw': {k: raw_data[k] for k in [
                'combat', 'connaissances', 'discretion', 'endurance', 'force',
                'habilete', 'magie', 'mouvement', 'perception', 'sociabilite',
                'survie', 'tir', 'volonte', 'race', 'is_important_npc', 'archetype'
            ] if k in raw_data},
            'computed': computed,
            'meta': {'updated_at': timezone.now().isoformat()}
        }

        attribute.model_brig = brig_data
        attribute.save()

        return Response({
            'attribute_id': attribute.id,
            'brigandyne': brig_data
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