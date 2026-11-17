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
    path("atividades/<int:pk>/", views.atividade_detalhe, name="atividade_detalhe"),
    path("atividades/<int:pk>/editar/", views.atividade_form, name="atividade_editar"),
    path("atividades/<int:pk>/ativa/", views.atividade_alternar_ativa, name="atividade_ativa"),
    path("atividades/<int:pk>/excluir/", views.atividade_excluir, name="atividade_excluir"),
    # Inscrições
    path("atividades/<int:atividade_pk>/inscrever/", views.inscricao_criar, name="inscricao_criar"),
    path("inscricoes/<int:pk>/cancelar/", views.inscricao_cancelar, name="inscricao_cancelar"),
    # Encontros
    path("atividades/<int:atividade_pk>/encontros/novo/", views.encontro_form, name="encontro_novo"),
    path("encontros/<int:pk>/editar/", views.encontro_form, name="encontro_editar"),
    path("encontros/<int:pk>/excluir/", views.encontro_excluir, name="encontro_excluir"),
    # Registro de presença
    path("presenca/", views.presenca_selecionar, name="presenca_selecionar"),
    path("presenca/encontro/<int:encontro_pk>/", views.presenca_registrar, name="presenca_registrar"),
    path("presenca/encontro/<int:encontro_pk>/resultado/", views.presenca_resultado, name="presenca_resultado"),
]
