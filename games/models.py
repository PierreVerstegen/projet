from django.db import models

import datetime
from django.db import models
from authentication.models import CustomUser



#TODO : =======CLASSE GAME===================


class Game(models.Model):
    """Class that manages game sessions or campaigns"""
    game_name = models.CharField(max_length = 100)

    class Theme(models.TextChoices):
        """Class describing different themes for games"""
        FANTASY = 'FANTASY', 'Fantasy'
        HORROR = 'HORROR', 'Horror'
        SCI_FI = 'SCI_FI', 'Science Fiction'
        HISTORICAL = 'HISTORICAL', 'Historical'
        CUSTOM = 'CUSTOM', 'Custom'



    game_theme = game_theme = models.CharField(
        max_length=20,
        choices=Theme.choices,
        default=Theme.FANTASY,
        help_text="Game theme"
    )

    

    game_started_on = models.DateTimeField(auto_now_add=True) 
#===============FOREIGN KEY ================================

    game_master_id = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name="games_mastered", help_text="Current GM for this game")
    #on_delete=models.PROTECT empêche la suppression d'un utilisateur si celui-ci est maître du jeu, 
    #ce qui est souvent souhaitable pour éviter de casser les relations.
    #related_name="games_mastered" permet d'accéder aux jeux maîtrisés par un utilisateur via user.games_mastered.all()



#============= MANY TO MANY ===============================
    players = models.ManyToManyField(
        'characters.Player',
        related_name="games", #permet d'accéder aux jeux associés à un joueur ou un PNJ via player.games.all() ou npc.games.all()
        blank=True,
        help_text="Players in the game."
    )
    npcs = models.ManyToManyField(
        'characters.NPC',
        related_name="games", #permet d'accéder aux jeux associés à un joueur ou un PNJ via player.games.all() ou npc.games.all()
        blank=True,
        help_text="NPC in the game."
    )

    #TODO : VERS USERS

#=============== META : tables, contraintes, indexes =============================
    class Meta:
        db_table = "games"
        constraints = [
            models.UniqueConstraint(
                fields=['game_name', 'game_master_id'],
                name='unique_game_name_per_master'
            )
        ]
        indexes = [
            models.Index(fields=['game_name']),
            models.Index(fields=['game_theme']),
        ]
#===============METHODS============================================================
       # Va-t-on utiliser des methods ou des views ? 
    def soft_delete(self):
        """Flags the entity as deleted => soft delete."""
        self.deleted_at = datetime.datetime.now()
        self.active = False
        self.save()




