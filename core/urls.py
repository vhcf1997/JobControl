from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    Remove-Item -Recurse -Force .gitpath('', views.index, name='index'),
    path('trabalhos/', views.lista_trabalhos, name='listar_trabalhos'),
    path('trabalhos/adicionar', views.add_trabalhos, name='add_trabalhos'),
    path('trabalhos/deletar/<int:pk>/', views.delete_trabalhos, name='delete_trabalhos'),
    path('trabalhos/editar/<int:pk>/', views.editar_trabalhos, name='editar_trabalhos'),
    path('register/', views.register_user, name='register'),
]