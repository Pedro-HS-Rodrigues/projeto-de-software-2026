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


class Atividade(models.Model):
    """Atividade oferecida pela associação (oficina, esporte, curso...)."""

    nome = models.CharField("nome", max_length=150)
    descricao = models.TextField("descrição", blank=True)
    ativa = models.BooleanField("ativa", default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "atividade"
        verbose_name_plural = "atividades"

    def __str__(self):
        return self.nome


class Inscricao(models.Model):
    """Vínculo do participante com uma atividade, sem repetir o cadastro dele."""

    class Status(models.TextChoices):
        ATIVA = "ativa", "Ativa"
        CANCELADA = "cancelada", "Cancelada"

    participante = models.ForeignKey(
        Participante, on_delete=models.PROTECT, related_name="inscricoes", verbose_name="participante"
    )
    atividade = models.ForeignKey(
        Atividade, on_delete=models.PROTECT, related_name="inscricoes", verbose_name="atividade"
    )
    data_inscricao = models.DateTimeField("data da inscrição", auto_now_add=True)
    status = models.CharField("situação", max_length=10, choices=Status.choices, default=Status.ATIVA)

    class Meta:
        ordering = ["participante__nome"]
        verbose_name = "inscrição"
        verbose_name_plural = "inscrições"
        constraints = [
            models.UniqueConstraint(fields=["participante", "atividade"], name="inscricao_unica_por_atividade"),
        ]

    def __str__(self):
        return f"{self.participante.nome} em {self.atividade.nome}"

    @property
    def ativa(self):
        return self.status == self.Status.ATIVA
