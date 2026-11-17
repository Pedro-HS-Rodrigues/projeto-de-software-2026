from django import forms

from .models import Atividade, Participante


class ParticipanteForm(forms.ModelForm):
    confirmar_duplicidade = forms.BooleanField(
        label="Confirmo que é outra pessoa e quero salvar mesmo assim",
        required=False,
    )

    class Meta:
        model = Participante
        fields = ["nome", "data_nascimento", "telefone_contato"]
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "telefone_contato": forms.TextInput(attrs={"type": "tel", "autocomplete": "off"}),
        }
        help_texts = {"telefone_contato": "Opcional."}

    def __init__(self, *args, mostrar_confirmacao=False, **kwargs):
        super().__init__(*args, **kwargs)
        if not mostrar_confirmacao:
            del self.fields["confirmar_duplicidade"]

    def clean_nome(self):
        nome = self.cleaned_data["nome"].strip()
        if not nome:
            raise forms.ValidationError("Informe o nome do participante.")
        return nome


class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = ["nome", "descricao", "ativa"]
        help_texts = {
            "descricao": "Opcional. Ex.: dias, horário e público da atividade.",
            "ativa": "Atividades inativas não recebem novas inscrições.",
        }
