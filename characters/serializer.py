from rest_framework import serializers
from .models import Character, NPC, Player, Attribute, Abilities, Effect
from django.contrib.auth import authenticate

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'
# je ne sais pas si c'est pertinent vu que c'est une classe abstraite mais bon

class NPCSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPC
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class AbilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abilities
        fields = '__all__'

class effectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Effect
        fields = '__all__'