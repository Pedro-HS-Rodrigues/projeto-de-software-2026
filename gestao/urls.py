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
]
