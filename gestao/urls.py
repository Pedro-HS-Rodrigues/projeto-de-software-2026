from django.urls import path

from . import views

urlpatterns = [
    path("", views.menu, name="menu"),
    # Participantes
    path("participantes/", views.participante_lista, name="participante_lista"),
    path("participantes/novo/", views.participante_form, name="participante_novo"),
    path("participantes/<int:pk>/editar/", views.participante_form, name="participante_editar"),
    path("participantes/<int:pk>/ativo/", views.participante_alternar_ativo, name="participante_ativo"),
    path("participantes/<int:pk>/excluir/", views.participante_excluir, name="participante_excluir"),
    # Atividades
    path("atividades/", views.atividade_lista, name="atividade_lista"),
    path("atividades/nova/", views.atividade_form, name="atividade_nova"),
    path("atividades/<int:pk>/editar/", views.atividade_form, name="atividade_editar"),
    path("atividades/<int:pk>/ativa/", views.atividade_alternar_ativa, name="atividade_ativa"),
    path("atividades/<int:pk>/excluir/", views.atividade_excluir, name="atividade_excluir"),
]
