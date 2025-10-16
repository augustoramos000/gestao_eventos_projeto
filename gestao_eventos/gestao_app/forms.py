# gestao_app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilUsuario, Evento

# ----------------------------------------------------------------------
# 1. Cadastro de Usuário (Requisito 1)
# ----------------------------------------------------------------------

class CadastroUsuarioForm(UserCreationForm):
    """Formulário para criar um novo usuário e seu PerfilUsuario associado."""
    
    telefone = forms.CharField(max_length=15, required=False)
    instituicao_ensino = forms.CharField(
        max_length=100, 
        required=False,
        help_text="Obrigatório para Alunos e Professores"
    )
    perfil = forms.ChoiceField(choices=PerfilUsuario.PERFIL_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'email') # Adicionando nome e email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
            # Cria o PerfilUsuario após o User ser salvo
            PerfilUsuario.objects.create(
                user=user,
                telefone=self.cleaned_data['telefone'],
                instituicao_ensino=self.cleaned_data['instituicao_ensino'],
                perfil=self.cleaned_data['perfil']
            )
        return user

# ----------------------------------------------------------------------
# 2. Cadastro de Evento (Requisito 2)
# ----------------------------------------------------------------------

class EventoForm(forms.ModelForm):
    """Formulário para criar e editar eventos."""
    
    class Meta:
        model = Evento
        # Excluímos 'organizador' e 'participantes' pois são preenchidos no backend
        fields = [
            'titulo', 'tipo', 'data_inicio', 'data_fim', 
            'local', 'quantidade_participantes'
        ]
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'data_fim': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }