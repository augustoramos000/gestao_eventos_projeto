from django import forms
# Já não precisamos da BaseUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario, Evento

class UserCreationForm(forms.ModelForm):
    """
    Um formulário para criar novos usuários, construído do zero para garantir controlo total
    sobre os nomes dos campos e a validação.
    """
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        help_text="A sua senha não pode ser muito parecida com o resto das suas informações pessoais."
    )
    password2 = forms.CharField(
        label="Confirmação da senha",
        widget=forms.PasswordInput,
        help_text="Digite a mesma senha novamente para confirmação."
    )

    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'telefone', 'instituicao_ensino', 'perfil')

    def clean_password2(self):
        # Validação para confirmar que as senhas são iguais
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("As senhas não correspondem.")
        return password2

    def save(self, commit=True):
        # Sobrescreve o método save para lidar com a senha (hashing)
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    pass

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        exclude = ['organizador_responsavel']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm'}),
            'data_fim': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm'}),
            'horario': forms.TimeInput(attrs={'type': 'time', 'class': 'mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm'}),
        }
    