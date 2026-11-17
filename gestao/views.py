"""Camada de apresentação: recebe as ações do usuário e devolve as telas."""
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from . import services
from .forms import AtividadeForm, InscricaoForm, ParticipanteForm
from .models import Atividade, Inscricao, Participante


def menu(request):
    return render(request, "gestao/menu.html")


# ---------------------------------------------------------------- Participantes

def participante_lista(request):
    termo = request.GET.get("q", "")
    participantes = services.buscar_participantes(termo)
    return render(request, "gestao/participante_lista.html", {"participantes": participantes, "termo": termo})


def participante_form(request, pk=None):
    participante = get_object_or_404(Participante, pk=pk) if pk else None
    duplicados = []

    if request.method == "POST":
        form = ParticipanteForm(request.POST, instance=participante, mostrar_confirmacao=True)
        if form.is_valid():
            duplicados = services.possiveis_duplicados(
                form.cleaned_data["nome"], form.cleaned_data["data_nascimento"], ignorar_id=pk
            )
            if duplicados.exists() and not form.cleaned_data.get("confirmar_duplicidade"):
                messages.warning(request, "Já existe participante com o mesmo nome e data de nascimento. Confira abaixo.")
            else:
                salvo = form.save()
                messages.success(request, f"Participante “{salvo.nome}” salvo.")
                return redirect("participante_lista")
    else:
        form = ParticipanteForm(instance=participante)

    if not duplicados:
        form.fields.pop("confirmar_duplicidade", None)
    return render(
        request,
        "gestao/participante_form.html",
        {"form": form, "participante": participante, "duplicados": duplicados},
    )


@require_POST
def participante_alternar_ativo(request, pk):
    participante = get_object_or_404(Participante, pk=pk)
    participante.ativo = not participante.ativo
    participante.save(update_fields=["ativo"])
    situacao = "reativado" if participante.ativo else "desativado"
    messages.success(request, f"Participante “{participante.nome}” {situacao}.")
    return redirect("participante_lista")


def participante_excluir(request, pk):
    participante = get_object_or_404(Participante, pk=pk)
    if request.method == "POST":
        try:
            participante.delete()
        except ProtectedError:
            messages.error(request, "Este participante tem histórico e não pode ser excluído. Desative o cadastro.")
        else:
            messages.success(request, f"Participante “{participante.nome}” excluído.")
        return redirect("participante_lista")
    return render(request, "gestao/confirmar_exclusao.html", {"objeto": participante, "voltar": "participante_lista"})


# ------------------------------------------------------------------ Atividades

def atividade_lista(request):
    return render(request, "gestao/atividade_lista.html", {"atividades": Atividade.objects.all()})


def atividade_detalhe(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)
    contexto = {
        "atividade": atividade,
        "inscricoes": atividade.inscricoes.select_related("participante"),
        "form_inscricao": InscricaoForm(participantes=services.participantes_disponiveis(atividade)),
    }
    return render(request, "gestao/atividade_detalhe.html", contexto)


def atividade_form(request, pk=None):
    atividade = get_object_or_404(Atividade, pk=pk) if pk else None
    form = AtividadeForm(request.POST or None, instance=atividade)
    if request.method == "POST" and form.is_valid():
        salva = form.save()
        messages.success(request, f"Atividade “{salva.nome}” salva.")
        return redirect("atividade_lista")
    return render(request, "gestao/atividade_form.html", {"form": form, "atividade": atividade})


@require_POST
def atividade_alternar_ativa(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)
    atividade.ativa = not atividade.ativa
    atividade.save(update_fields=["ativa"])
    situacao = "reativada" if atividade.ativa else "desativada"
    messages.success(request, f"Atividade “{atividade.nome}” {situacao}.")
    return redirect("atividade_lista")


def atividade_excluir(request, pk):
    atividade = get_object_or_404(Atividade, pk=pk)
    if request.method == "POST":
        try:
            atividade.delete()
        except ProtectedError:
            messages.error(request, "Esta atividade tem histórico e não pode ser excluída. Desative a atividade.")
        else:
            messages.success(request, f"Atividade “{atividade.nome}” excluída.")
        return redirect("atividade_lista")
    return render(request, "gestao/confirmar_exclusao.html", {"objeto": atividade, "voltar": "atividade_lista"})


# ------------------------------------------------------------------ Inscrições

@require_POST
def inscricao_criar(request, atividade_pk):
    atividade = get_object_or_404(Atividade, pk=atividade_pk)
    form = InscricaoForm(request.POST, participantes=Participante.objects.all())
    if form.is_valid():
        try:
            inscricao = services.inscrever(form.cleaned_data["participante"], atividade)
        except services.RegraDeNegocioError as erro:
            messages.error(request, str(erro))
        else:
            messages.success(request, f"{inscricao.participante.nome} inscrito(a) em {atividade.nome}.")
    else:
        messages.error(request, "Selecione um participante para inscrever.")
    return redirect("atividade_detalhe", pk=atividade.pk)


@require_POST
def inscricao_cancelar(request, pk):
    inscricao = get_object_or_404(Inscricao.objects.select_related("participante", "atividade"), pk=pk)
    try:
        services.cancelar_inscricao(inscricao)
    except services.RegraDeNegocioError as erro:
        messages.error(request, str(erro))
    else:
        messages.success(request, f"Inscrição de {inscricao.participante.nome} cancelada. O histórico foi mantido.")
    return redirect("atividade_detalhe", pk=inscricao.atividade_id)
