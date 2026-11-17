"""Camada de apresentação: recebe as ações do usuário e devolve as telas."""
from django.shortcuts import render


def menu(request):
    return render(request, "gestao/menu.html")
