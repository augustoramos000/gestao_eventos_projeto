from django import forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, AuthenticationForm
from .models import Usuario, Evento

class UserCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'telefone', 'instituicao_ensino', 'perfil')

class LoginForm(AuthenticationForm):
    pass

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = '__all__'