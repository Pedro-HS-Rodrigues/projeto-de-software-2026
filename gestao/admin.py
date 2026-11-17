from django.contrib import admin

from .models import Atividade, Participante


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ["nome", "data_nascimento", "telefone_contato", "ativo"]
    list_filter = ["ativo"]
    search_fields = ["nome"]


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ["nome", "ativa"]
    list_filter = ["ativa"]
    search_fields = ["nome"]
