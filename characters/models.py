from django.db import models

from django.db import models
from authentication.models import CustomUser

from django.core.validators import MinValueValidator #cette fcionalité m'a été suggérée par IA

#TODO : ===========CECI EST UNE CLASSE ABSTRAITE PARENTE DE NPC ET PLAYER===============

class Character(models.Model):# On utilise ABC pour indiquer que cette classe est abstraite ; NPC et Player en héritent.
    """Abstract class for characters in a Game. Parent to NPC and Player classes"""

# ========== Choice Fields ================
  # # Stockez les constantes dans une classe : Définissez les choix comme une constante (par exemple, STATUT_CHOICES) 
# pour une meilleure réutilisation.
# # Utilisez TextChoices (Django 3.0+) : Pour une syntaxe plus moderne, vous pouvez utiliser une classe 
# # TextChoices pour définir les choix :  
    
    class Charac_model(models.TextChoices):
        """Supported game systems"""
        DND = 'DND', 'Dungeons & Dragons'
        CTHULHU = 'CTHU', 'Call of Cthulhu'
        BRIG = 'BRIG', 'Brigandyne'
        DCC = 'DCC', 'Dungeon Crawler Classic'
        HMB = 'HMB', 'Homebrew system'

#Ici on définit les options pour le modele qu'utilisera le personnage
# Avec TextChoices, les choix sont mieux organisés, et vous pouvez accéder aux valeurs comme Character.Charac_model.DND.

# ============== CLASS ATTRIBUTES ==================
    charac_name=models.CharField(max_length = 100)
    charac_class=models.CharField(max_length = 100)
    charac_lvl=models.IntegerField(validators=[MinValueValidator(1)])
    charac_hp=models.IntegerField(validators=[MinValueValidator(0)])
    charac_money=models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default = 0.00)
    charac_model=models.CharField(max_length=10, choices=Charac_model.choices, default=Charac_model.DND,)
    charac_bio=models.TextField(blank=True, default="")
    
    
 #===============FOREIGN KEY ================================   
    user_id=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="%(class)s_characters") #ForeignKey Vers User
    #selon l'IA : Ajouter related_name="characters" permet d'accéder aux personnages associés à un utilisateur via user.characters.all()
    

#=============== META : tables, contraintes, indexes ========================
    class Meta:
            abstract = True



#TODO : =======CLASSES ENFANT : NPC ===================



class NPC(Character):
    """For the GM only"""
# ============== CLASS ATTRIBUTES ==================
    is_hostile = models.BooleanField(default=False)
    faction = models.CharField(max_length=100, blank=True)

#============= MANY TO MANY ===============================
    abilities = models.ManyToManyField(
        'Abilities',
        related_name="npc",
        blank=True,
        help_text="Abilities possessed by this NPC.")

#=============== META : tables, contraintes, indexes ========================
    class Meta:
        db_table = "npcs"  # Nom de la table dans la base de données ---> vient de l'IA ; à vérifier
        abstract = False


#TODO : =======CLASSES ENFANT : PLAYER ===================



class Player(Character):
    """Represent one playable character"""
# ============== CLASS ATTRIBUTES ==================
    experience_points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
#============= MANY TO MANY ===============================
    abilities = models.ManyToManyField(
        'Abilities',
        related_name="player",
        blank=True,
        help_text="Abilities possessed by this player.")
    

#=============== META : tables, contraintes, indexes ==========================
    class Meta:
        db_table = "players"  # Nom de la table dans la base de données ---> vient de l'IA ; à vérifier
        abstract = False

#TODO : =======ATTRIBUTES, ABILITIES AND EFFECTS===================

class Attribute(models.Model):
    """Contains models for characters following different rule systems"""

# ============== CLASS ATTRIBUTES ==================
    
    model_dnd=models.JSONField(default=dict, blank = True)
    model_cthulhu=models.JSONField(default=dict, blank = True)
    model_brig=models.JSONField(default=dict, blank = True)
    model_dcc=models.JSONField(default=dict, blank = True)
    model_homebrew=models.JSONField(default=dict, blank = True)
    
#============= MANY TO MANY ===============================
    
    players = models.ManyToManyField(
        'Player',
        related_name="attributes", #permet d'accéder aux jeux associés à un joueur ou un PNJ via player.games.all() ou npc.games.all()
        blank=True,
        help_text="Players in the game."
    )
    npcs = models.ManyToManyField(
        'NPC',
        related_name="attributes", #permet d'accéder aux jeux associés à un joueur ou un PNJ via player.games.all() ou npc.games.all()
        blank=True,
        help_text="NPC in the game."
    )



class Abilities(models.Model): #On va devoir peupler la table avec ttes les abilities de ces 5 systèmes de jeu
    """Contains Abilities possessed by characters"""
# ========== Choice Fields ============================
# On réutilise la classe de choix pour la variable ability_source
    
    class Ability_source(models.TextChoices):
        DND = 'DND', 'Dungeons & Dragons'
        CTHULHU = 'CTHU', 'Call of Cthulhu'
        BRIG = 'BRIG', 'Brigandyne'
        DCC = 'DCC', 'Dungeon Crawler Classic'
        HMB = 'HMB', 'Homebrew system'

# ============== CLASS ABILITIES ==================
    ability_name = models.CharField(max_length = 200)
    ability_source = models.CharField(max_length=10, choices=Ability_source.choices, default=Ability_source.DND,)
    ability_description = models.TextField(blank=True, default="")
    ability_class = models.CharField(max_length = 200) #Pour l'instant on utilise un simple charField, mais à terme ce serait 
    #                                                     bien d'utiliser la même méthode de choix ; il faudrait stocker les différents choix quelque part

#============= MANY TO MANY ===============================
    effect = models.ManyToManyField(
        'Effect',
        related_name="ability",
        blank=True,
        help_text="Effects possessed by this ability.")

#========== META : tables, contraintes, indexes ============
    class Meta:
        db_table = 'abilities'
    


class Effect(models.Model):
    """Describes different effects for different abilities"""

# ============== CLASS EFFECTS ==================
    effect_name = models.CharField(max_length = 200)
    effect_description = models.TextField(blank=True, default="")





#============================= DEV NOTES =============================================================================================
            #Puisque Character hérite de ABC, vous pouvez définir des méthodes abstraites que NPC et Player doivent implémenter. 
            #Cela garantit que chaque sous-classe fournit une implémentation spécifique pour certains comportements.
            #Pourquoi ? -> Les méthodes abstraites garantissent que chaque sous-classe définit son propre comportement, 
            # #renforçant la cohérence du code.
            # -> utiliser le décorateur @abstractmethod
#==========================================================================================================================