from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('trabalhos/', views.lista_trabalhos, name='listar_trabalhos'),
    path('trabalhos/adicionar', views.add_trabalhos, name='add_trabalhos'),
    path('trabalhos/deletar/<int:pk>/', views.delete_trabalhos, name='delete_trabalhos'),
    path('trabalhos/editar/<int:pk>/', views.editar_trabalhos, name='editar_trabalhos'),
    path('projetos/', views.lista_projetos, name='listar_projetos'),
    path('projetos/adicionar', views.add_projetos, name='add_projetos'),
    path('projetos/deletar/<int:pk>/', views.delete_projetos, name='delete_projetos'),
    path('projetos/editar/<int:pk>/', views.editar_projetos, name='editar_projetos'),
    path('register/', views.register_user, name='register'),
]