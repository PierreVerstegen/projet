from django.urls import path, include
from rest_framework.routers import DefaultRouter
from games.views import GameViewset

router = DefaultRouter()    



router.register(r'games', GameViewset, basename='game')

urlpatterns = [
    path('api/', include(router.urls))
    
]