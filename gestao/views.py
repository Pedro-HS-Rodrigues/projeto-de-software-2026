"""Camada de apresentação: recebe as ações do usuário e devolve as telas."""
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from . import services
from .forms import ParticipanteForm
from .models import Participante


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
