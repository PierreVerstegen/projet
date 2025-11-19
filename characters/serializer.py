from rest_framework import serializers

from authentication.serializers import UserSerializer
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
# ================================== CUSTOM SERIALIZERS=========================================

from rest_framework import serializers
from .models import Attribute

# class BrigandyneAttributeSerializer(serializers.Serializer):
    # Attributs de base (envoyés par le front)
    # combat = serializers.IntegerField(min_value=0, max_value=100)
    # connaissances = serializers.IntegerField(min_value=0, max_value=100)
    # discretion = serializers.IntegerField(min_value=0, max_value=100)
    # endurance = serializers.IntegerField(min_value=0, max_value=100)
    # force = serializers.IntegerField(min_value=0, max_value=100)
    # habilete = serializers.IntegerField(min_value=0, max_value=100)
    # magie = serializers.IntegerField(min_value=0, max_value=50)  # max 50
    # mouvement = serializers.IntegerField(min_value=0, max_value=100)
    # perception = serializers.IntegerField(min_value=0, max_value=100)
    # sociabilite = serializers.IntegerField(min_value=0, max_value=100)
    # survie = serializers.IntegerField(min_value=0, max_value=100)
    # tir = serializers.IntegerField(min_value=0, max_value=100)
    # volonte = serializers.IntegerField(min_value=0, max_value=100)

    # # Métadonnées
    # race = serializers.CharField(max_length=50, allow_blank=True, required=False)
    # archetype = serializers.CharField(max_length=100, allow_blank=True, required=False)

    # # Attributs calculés (ReadOnly)
    # pv = serializers.SerializerMethodField()
    # sang_froid = serializers.SerializerMethodField()
    # init = serializers.SerializerMethodField()
    # points_fortune = serializers.SerializerMethodField()

    # # === MÉTHODES DE CALCUL ===
    # def get_pv(self, obj):
    #     base = obj['endurance'] // 5 + obj['force'] // 5
    #     base + obj['volonte'] // 5
    #     return base

    # def get_sang_froid(self, obj):
    #     return (obj['volonte'] // 5) + (obj['connaissances'] // 5) + (obj.get('bonus_combat', 0) or 0)

    # def get_init(self, obj):
    #     # à fixer : bonus_combat etc n'existent pas, il s'agit de la dizaine de la stat en question
    #     return (obj.get('bonus_combat', 0) or 0) + (obj.get('bonus_mouvement', 0) or 0) + (obj.get('bonus_perception', 0) or 0)

    # def get_points_fortune(self, obj):
    #     return obj['volonte'] // 5

    # # === VALIDATION MÉTIER ===
    # def validate(self, data):
    #     # 1. Magie ≤ 50
    #     if data['magie'] > 50:
    #         raise serializers.ValidationError({"magie": "La magie ne peut dépasser 50."})

    #     # 2. Aucune stat < 15 (sauf magie qui peut être 0)
    #     min_stats = ['combat', 'connaissances', 'discretion', 'endurance', 'force',
    #                 'habilete', 'mouvement', 'perception', 'sociabilite', 'survie', 'tir', 'volonte']
    #     for stat in min_stats:
    #         if data[stat] < 15 and stat != 'magie':
    #             raise serializers.ValidationError({stat: f"{stat.capitalize()} ne peut être inférieur à 15."})

    #     # 3. Bonus de race (exemple)
    #     race = data.get('race', '').lower()
    #     base_stats = {
    #         'humain': 25, 'elfe': 20, 'nain': 30, 'orc': 35
    #         # etc.
    #     }
    #     expected_base = base_stats.get(race, 25)
    #     # Tu pourrais valider que les stats sont cohérentes avec 2d10 + base, mais c'est optionnel

    #     return data

    # # === SAUVEGARDE DANS model_brig ===
    # def save_to_attribute(self, attribute_instance):
    #     data = self.validated_data

    #     # Dictionnaire PLAT
    #     brig_data = {
    #         # Stats brutes
    #         'combat': data['combat'],
    #         'connaissances': data['connaissances'],
    #         'discretion': data['discretion'],
    #         'endurance': data['endurance'],
    #         'force': data['force'],
    #         'habilete': data['habilete'],
    #         'magie': data['magie'],
    #         'mouvement': data['mouvement'],
    #         'perception': data['perception'],
    #         'sociabilite': data['sociabilite'],
    #         'survie': data['survie'],
    #         'tir': data['tir'],
    #         'volonte': data['volonte'],

    #         # Métadonnées
    #         'race': data.get('race', ''),
    #         'archetype': data.get('archetype', ''),

    #         # Calculés
    #         'pv': self.get_pv(None),
    #         'sang_froid': self.get_sang_froid(None),
    #         'init': self.get_init(None)
    #     }


    #     # Sauvegarde dans le JSONField
    #     attribute_instance.model_brig = brig_data
    #     attribute_instance.save()
    #     return brig_data
    
    # def to_internal_value(self, data):
    #     # Permet d'utiliser le serializer comme un ModelSerializer
    #     return super().to_internal_value(data)
    
class BrigandyneCreateSerializer(serializers.Serializer):
    # === Données de base ===
    charac_name = serializers.CharField(max_length=100)
    charac_class = serializers.CharField(max_length=100)
    charac_lvl = serializers.IntegerField(min_value=1, required=False, default=1)
    charac_money = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    charac_bio = serializers.CharField(required=False, default="")

    # === Attributs Brigandyne ===
    combat = serializers.IntegerField(min_value=0, max_value=100)
    connaissances = serializers.IntegerField(min_value=0, max_value=100)
    discretion = serializers.IntegerField(min_value=0, max_value=100)
    endurance = serializers.IntegerField(min_value=0, max_value=100)
    force = serializers.IntegerField(min_value=0, max_value=100)
    habilete = serializers.IntegerField(min_value=0, max_value=100)
    magie = serializers.IntegerField(min_value=0, max_value=50)  # max 50
    mouvement = serializers.IntegerField(min_value=0, max_value=100)
    perception = serializers.IntegerField(min_value=0, max_value=100)
    sociabilite = serializers.IntegerField(min_value=0, max_value=100)
    survie = serializers.IntegerField(min_value=0, max_value=100)
    tir = serializers.IntegerField(min_value=0, max_value=100)
    volonte = serializers.IntegerField(min_value=0, max_value=100)

    # Métadonnées
    race = serializers.CharField(max_length=50, allow_blank=True, required=False)
    archetype = serializers.CharField(max_length=100, allow_blank=True, required=False)

    # Attributs calculés (ReadOnly)
    pv = serializers.SerializerMethodField()
    sang_froid = serializers.SerializerMethodField()
    init = serializers.SerializerMethodField()
    points_fortune = serializers.SerializerMethodField()
    abilities = serializers.ListField(child=serializers.CharField(max_length=200), required=False)

    # === Computed attributes ===
    def get_pv(self, data):
        base = data['endurance'] // 5 + data['force'] // 5 + data['volonte'] // 5
        return base
    
    def get_sang_froid(self, obj):
        return (obj['volonte'] // 5) + (obj['connaissances'] // 5) + (obj['combat']//10, 0 or 0)
    
    def get_init(self, obj):
        # Tu peux enrichir avec bonus d'archétype plus tard
        return (obj['combat']//10 or 0) + (obj['mouvement']//10 or 0) + (obj['perception']//10 or 0)
    


    def validate(self, data):
        # Magie ≤ 50
        if data['magie'] > 50:
            raise serializers.ValidationError({"magie": "Max 50"})

        # Stats ≥ 15 (other than magie)
        for field in ['combat', 'connaissances', 'discretion', 'endurance', 'habilete', 'force', 'mouvement', 'perception', 'sociabilite', 'survie', 'tir', 'volonte']:
            if data[field] < 15:
                raise serializers.ValidationError({field: "Min 15"})

        # Check abilities
        if 'abilities' in data:
            missing = set(data['abilities']) - set(
                Abilities.objects.filter(
                    ability_name__in=data['abilities'],
                    ability_source='BRIG'
                ).values_list('ability_name', flat=True)
            )
            if missing:
                raise serializers.ValidationError({"abilities": f"Could not be found : {missing}"})

        return data

    # === SAUVEGARDE DANS model_brig ===
    def save_to_attribute(self, attribute_instance):
        """
        Sauvegarde les données validées + calculées dans model_brig
        """
        # Copie des données brutes
        brig_data = {
            'raw': {k: v for k, v in self.validated_data.items() if k in [
                'combat', 'connaissances', 'discretion', 'endurance', 'force', 'habilete',
                'magie', 'mouvement', 'perception', 'sociabilite', 'survie', 'tir', 'volonte',
                'race', 'archetype'
            ]},
            'computed': {
                'pv': self.get_pv(self.validated_data),
                'sang_froid': self.get_sang_froid(self.validated_data),
                'init': self.get_init(self.validated_data),
            }
        }

        # Sauvegarde dans le JSONField
        attribute_instance.model_brig = brig_data
        attribute_instance.save()
        return brig_data
    
    def to_internal_value(self, data):
        # Permet d'utiliser le serializer comme un ModelSerializer
        return super().to_internal_value(data)