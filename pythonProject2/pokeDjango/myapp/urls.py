from django.urls import path
from . import views

urlpatterns = [
    path('pokemon/<int:id>/', views.pokemon, name='pokemon'),
    path('ability/<int:id>/', views.ability, name='ability'),
    path('name/', views.name, name='name'),
    path('team/', views.team, name='team'),
    path('setTeam/<int:id>', views.setTeam, name='setTeam'),
    path('', views.index, name='index'),
    path('fr', views.index_fr, name='index_fr'),
    path('en', views.index, name='index')
]
