
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from characters.views import BrigandyneCharacterViewSet, NPCViewset, PlayerViewset, AttributeViewset, AbilitiesViewset, EffectViewset

router = DefaultRouter()    



router.register(r'npcs', NPCViewset, basename='npc')
router.register(r'players', PlayerViewset, basename='player')
router.register(r'attributes', AttributeViewset, basename='attribute')
router.register(r'abilities', AbilitiesViewset, basename='ability')
router.register(r'effects', EffectViewset, basename='effect')
router.register(r'characters/brigandyne', BrigandyneCharacterViewSet, basename='brigandyne-character')

urlpatterns = [
    path('api/', include(router.urls))
    
]

