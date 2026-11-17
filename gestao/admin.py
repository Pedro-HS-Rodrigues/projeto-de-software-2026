from django.contrib import admin

from .models import Participante


@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    list_display = ["nome", "data_nascimento", "telefone_contato", "ativo"]
    list_filter = ["ativo"]
    search_fields = ["nome"]
