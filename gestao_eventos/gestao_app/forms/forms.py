from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from .models import Usuario, Evento

# Formulário de criação de usuário customizado
class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'telefone', 'instituicao_ensino', 'perfil')
        help_texts = {
            'username': None,
        }

# Formulário de Login
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md', 'placeholder': 'Seu usuário'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md', 'placeholder': 'Sua senha'}), required=True)

# Formulário para criar e editar eventos
class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome', 'tipo_evento', 'data_inicio', 'data_fim', 'horario', 'local', 'quantidade_participantes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'tipo_evento': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded-md bg-white'}),
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border rounded-md'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 border rounded-md'}),
            'horario': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full px-3 py-2 border rounded-md'}),
            'local': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
            'quantidade_participantes': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}),
        }
