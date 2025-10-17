from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Evento, Inscricao, Usuario
from .forms import UserCreationForm, LoginForm, EventoForm

def listar_eventos(request):
    eventos = Evento.objects.all().order_by('data_inicio')
    eventos_inscritos_ids = []
    if request.user.is_authenticated:
        eventos_inscritos_ids = Inscricao.objects.filter(usuario=request.user).values_list('evento_id', flat=True)

    contexto = {
        'eventos': eventos,
        'eventos_inscritos_ids': list(eventos_inscritos_ids)
    }
    return render(request, 'gestao_app/listar_eventos.html', contexto)

def cadastro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('listar_eventos')
        else:
            # ADICIONE ESTAS LINHAS PARA DEPURAÇÃO
            print("--- ERROS DE VALIDAÇÃO DO FORMULÁRIO DE CADASTRO ---")
            print(form.errors.as_json())
            # FIM DAS LINHAS DE DEPURAÇÃO
            messages.error(request, 'Ocorreram erros no formulário. Por favor, corrija-os.')
    else:
        form = UserCreationForm()
    return render(request, 'gestao_app/cadastro.html', {'form': form})

def login_usuario(request):
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
    return render(request, 'gestao_app/login.html', {'form': form})

@login_required
def logout_usuario(request):
    logout(request)
    return redirect('listar_eventos')

@login_required
def minhas_inscricoes(request):
    inscricoes = Inscricao.objects.filter(usuario=request.user).select_related('evento')
    return render(request, 'gestao_app/minhas_inscricoes.html', {'inscricoes': inscricoes})

@login_required
def inscrever_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    Inscricao.objects.get_or_create(usuario=request.user, evento=evento)
    messages.success(request, f'Inscrição no evento "{evento.nome}" realizada com sucesso!')
    return redirect('listar_eventos')

@login_required
def criar_evento(request):
    if request.user.perfil != 'ORGANIZADOR':
        messages.error(request, 'Você não tem permissão para criar eventos.')
        return redirect('listar_eventos')

    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador_responsavel = request.user
            evento.save()
            messages.success(request, 'Evento criado com sucesso!')
            return redirect('listar_eventos')
        else:
            messages.error(request, 'Ocorreram erros no formulário. Por favor, corrija-os.')
    else:
        form = EventoForm()
    
    return render(request, 'gestao_app/criar_evento.html', {'form': form})

@login_required
def emitir_certificado(request, inscricao_id):
    pass

