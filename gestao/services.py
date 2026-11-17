"""
Camada de regras de negócio.

As telas (views) chamam estas funções; elas validam as condições de cada
operação e usam o ORM (models) para consultar ou gravar os dados.
"""
from .models import Participante


class RegraDeNegocioError(Exception):
    """Operação recusada por uma regra do sistema; a mensagem é mostrada ao usuário."""


def possiveis_duplicados(nome, data_nascimento, ignorar_id=None):
    """RF02: participantes com mesmo nome e nascimento, para conferência (sem bloqueio)."""
    duplicados = Participante.objects.filter(nome__iexact=nome.strip(), data_nascimento=data_nascimento)
    if ignorar_id:
        duplicados = duplicados.exclude(pk=ignorar_id)
    return duplicados


def buscar_participantes(termo):
    """RF03: pesquisa por parte do nome."""
    participantes = Participante.objects.all()
    if termo:
        participantes = participantes.filter(nome__icontains=termo.strip())
    return participantes
