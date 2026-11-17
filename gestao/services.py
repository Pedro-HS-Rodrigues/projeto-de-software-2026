"""
Camada de regras de negócio.

As telas (views) chamam estas funções; elas validam as condições de cada
operação e usam o ORM (models) para consultar ou gravar os dados.
"""
from django.db import transaction

from .models import Inscricao, Participante


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


# ------------------------------------------------------------------ Inscrições

@transaction.atomic
def inscrever(participante, atividade):
    """
    RF05: inscreve o participante na atividade.

    Participante e atividade precisam estar ativos e a combinação é única:
    uma inscrição ativa repetida é recusada; uma cancelada é reativada,
    sem criar outro registro.
    """
    if not participante.ativo:
        raise RegraDeNegocioError("O participante está inativo e não pode receber novas inscrições.")
    if not atividade.ativa:
        raise RegraDeNegocioError("A atividade está inativa e não aceita novas inscrições.")

    existente = Inscricao.objects.select_for_update().filter(participante=participante, atividade=atividade).first()
    if existente:
        if existente.ativa:
            raise RegraDeNegocioError(f"{participante.nome} já está inscrito(a) em {atividade.nome}.")
        existente.status = Inscricao.Status.ATIVA
        existente.save(update_fields=["status"])
        return existente
    return Inscricao.objects.create(participante=participante, atividade=atividade)


def cancelar_inscricao(inscricao):
    """O cancelamento mantém o registro e as presenças anteriores."""
    if not inscricao.ativa:
        raise RegraDeNegocioError("Esta inscrição já está cancelada.")
    inscricao.status = Inscricao.Status.CANCELADA
    inscricao.save(update_fields=["status"])
    return inscricao


def participantes_disponiveis(atividade):
    """Participantes ativos que ainda não têm inscrição ativa na atividade."""
    inscritos = atividade.inscricoes.filter(status=Inscricao.Status.ATIVA).values("participante_id")
    return Participante.objects.filter(ativo=True).exclude(pk__in=inscritos)
