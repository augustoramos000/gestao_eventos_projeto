from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Evento, Inscricao, Usuario
from .forms import UserCreationForm, LoginForm

# NOTA: Os formulários de evento, inscrição, etc., não foram implementados
# e seriam necessários para a funcionalidade completa.

def listar_eventos(request):
    """
    View para listar todos os eventos disponíveis.
    """
    eventos = Evento.objects.all().order_by('data_inicio')
    eventos_inscritos_ids = []
    if request.user.is_authenticated:
        # Pega os IDs dos eventos em que o usuário já está inscrito
        eventos_inscritos_ids = Inscricao.objects.filter(usuario=request.user).values_list('evento_id', flat=True)

    contexto = {
        'eventos': eventos,
        'eventos_inscritos_ids': list(eventos_inscritos_ids)
    }
    # CORREÇÃO: O caminho do template foi ajustado para usar 'gestao_app/'
    return render(request, 'gestao_app/listar_eventos.html', contexto)

def cadastro_usuario(request):
    """
    View para registrar um novo usuário.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('listar_eventos')
    else:
        form = UserCreationForm()
    # CORREÇÃO: O caminho do template foi ajustado
    return render(request, 'gestao_app/cadastro.html', {'form': form})

def login_usuario(request):
    """
    View para autenticar um usuário.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('listar_eventos')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginForm()
    # CORREÇÃO: O caminho do template foi ajustado
    return render(request, 'gestao_app/login.html', {'form': form})

@login_required
def logout_usuario(request):
    """
    View para fazer logout do usuário.
    """
    logout(request)
    return redirect('listar_eventos')

@login_required
def minhas_inscricoes(request):
    """
    View para o usuário ver os eventos em que está inscrito.
    """
    inscricoes = Inscricao.objects.filter(usuario=request.user).select_related('evento')
    # CORREÇÃO: O caminho do template foi ajustado
    return render(request, 'gestao_app/minhas_inscricoes.html', {'inscricoes': inscricoes})

# As views abaixo são placeholders e precisariam de mais lógica

@login_required
def inscrever_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    # Lógica para criar a inscrição aqui...
    Inscricao.objects.get_or_create(usuario=request.user, evento=evento)
    messages.success(request, f'Inscrição no evento "{evento.nome}" realizada com sucesso!')
    return redirect('listar_eventos')

@login_required
def criar_evento(request):
    # Lógica para criar um novo evento aqui...
    # Esta view precisaria de um formulário (EventoForm) e um template (criar_evento.html)
    pass

@login_required
def emitir_certificado(request, inscricao_id):
    # Lógica para gerar e emitir um certificado aqui...
    pass
