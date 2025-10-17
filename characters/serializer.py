from rest_framework import serializers
from .models import Character, NPC, Player, Attribute, Abilities, Effect
from django.contrib.auth import authenticate

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'
        read_only_fields = ['user_id'] #empechera au user de fournir ce champs dans la requete puisque nous voulons le remplir nous-meme
# je ne sais pas si c'est pertinent vu que c'est une classe abstraite mais bon

class NPCSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPC
        fields = '__all__'
        read_only_fields = ['user_id']
class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
        read_only_fields = ['user_id']
class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class AbilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abilities
        fields = '__all__'

class EffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Effect
        fields = '__all__'