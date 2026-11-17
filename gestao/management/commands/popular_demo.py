"""
Carrega dados FICTÍCIOS para demonstração e validação com a associação.

Uso:  python manage.py popular_demo
Não use com dados reais de moradores.
"""
from datetime import date, datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from gestao import services
from gestao.models import Atividade, Encontro, Participante


class Command(BaseCommand):
    help = "Carrega participantes, atividades, encontros e presenças fictícios para demonstração."

    @transaction.atomic
    def handle(self, *args, **opcoes):
        fuso = timezone.get_current_timezone()

        leitura, _ = Atividade.objects.get_or_create(
            nome="Oficina de leitura", defaults={"descricao": "Sextas-feiras, 14h. Crianças de 7 a 12 anos."}
        )
        futebol, _ = Atividade.objects.get_or_create(
            nome="Escolinha de futebol", defaults={"descricao": "Sábados, 8h. Adolescentes."}
        )

        a, _ = Participante.objects.get_or_create(nome="Pessoa Exemplo A", defaults={"data_nascimento": date(2014, 4, 10)})
        b, _ = Participante.objects.get_or_create(nome="Pessoa Exemplo B", defaults={"data_nascimento": date(2015, 8, 22)})
        c, _ = Participante.objects.get_or_create(
            nome="Pessoa Exemplo C", defaults={"data_nascimento": date(2010, 1, 5), "telefone_contato": "(85) 90000-0000"}
        )

        inscricoes = {}
        for participante, atividade in [(a, leitura), (b, leitura), (a, futebol), (c, futebol)]:
            try:
                inscricoes[(participante.pk, atividade.pk)] = services.inscrever(participante, atividade)
            except services.RegraDeNegocioError:
                inscricoes[(participante.pk, atividade.pk)] = participante.inscricoes.get(atividade=atividade)

        e1, _ = Encontro.objects.get_or_create(
            atividade=leitura, inicio=datetime(2026, 11, 13, 14, 0, tzinfo=fuso), defaults={"status": "realizado"}
        )
        Encontro.objects.get_or_create(
            atividade=leitura, inicio=datetime(2026, 11, 20, 14, 0, tzinfo=fuso), defaults={"status": "realizado"}
        )
        e3, _ = Encontro.objects.get_or_create(
            atividade=futebol, inicio=datetime(2026, 11, 14, 8, 0, tzinfo=fuso), defaults={"status": "realizado"}
        )

        services.registrar_presencas(e1, {inscricoes[(a.pk, leitura.pk)].pk: "presente", inscricoes[(b.pk, leitura.pk)].pk: "presente"})
        services.registrar_presencas(e3, {inscricoes[(a.pk, futebol.pk)].pk: "faltou", inscricoes[(c.pk, futebol.pk)].pk: "presente"})

        self.stdout.write(self.style.SUCCESS("Dados fictícios carregados. O encontro de 20/11/2026 ficou sem chamada para a demonstração."))
