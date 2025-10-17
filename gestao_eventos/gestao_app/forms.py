from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, AuthenticationForm
from .models import Usuario, Evento

class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'telefone', 'instituicao_ensino', 'perfil')

class LoginForm(AuthenticationForm):
    pass

# CORREÇÃO APLICADA AQUI
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        # Em vez de listar os campos a incluir, excluímos o que não queremos no formulário.
        # Isto informa ao Django para não se preocupar com a validação deste campo.
        exclude = ['organizador_responsavel']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm'}),
            'horario': forms.TimeInput(attrs={'type': 'time', 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm'}),
        }

