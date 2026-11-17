"""Camada de persistência: entidades do MVP mapeadas pelo ORM do Django."""
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


def nao_pode_ser_futura(data):
    if data and data > timezone.localdate():
        raise ValidationError("A data de nascimento não pode ser no futuro.")


class Participante(models.Model):
    """Cadastro único do morador atendido pela associação."""

    nome = models.CharField("nome", max_length=150)
    data_nascimento = models.DateField("data de nascimento", validators=[nao_pode_ser_futura])
    telefone_contato = models.CharField("telefone de contato", max_length=20, blank=True)
    ativo = models.BooleanField("ativo", default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "participante"
        verbose_name_plural = "participantes"

    def __str__(self):
        return f"{self.nome} ({self.data_nascimento:%d/%m/%Y})"
