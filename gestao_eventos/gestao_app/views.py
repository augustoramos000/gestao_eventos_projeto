# gestao_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.contrib import messages
from django.utils import timezone
import uuid # Para gerar códigos de certificado

# Importações dos Modelos e Formulários
from .models import Evento, PerfilUsuario, Certificado
from .forms import CadastroUsuarioForm, EventoForm


# --- ROTAS DE NAVEGAÇÃO ---

def index(request):
    """Página inicial com listagem de eventos disponíveis."""
    eventos_disponiveis = Evento.objects.filter(data_fim__gte=timezone.now()).order_by('data_inicio')
    context = {
        'eventos': eventos_disponiveis,
    }
    return render(request, 'index.html', {})

# --- AUTENTICAÇÃO E CADASTRO (Requisitos 1 e 5) ---

def cadastro_usuario(request):
    """Requisito 1: Cadastro de usuários (Aluno, Professor, Organizador)."""
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso! Bem-vindo(a).')
            return redirect('index') 
    else:
        form = CadastroUsuarioForm()
    return render(request, 'cadastro.html', {'form': form})

def login_usuario(request):
    """Requisito 5: Autenticação de usuários."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo(a) de volta, {user.username}.')
            return redirect('index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_usuario(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('index')


# --- CRIAÇÃO E GERENCIAMENTO DE EVENTOS (Requisito 2) ---

@login_required
def criar_evento(request):
    """Requisito 2: Criação de eventos (Apenas para ORGANIZADORES)."""
    # Verifica se o usuário logado é um Organizador
    if request.user.perfilusuario.perfil != 'ORGANIZADOR':
        messages.error(request, 'Acesso negado. Apenas organizadores podem criar eventos.')
        return redirect('index')

    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            # Define o organizador como o PerfilUsuario logado
            evento.organizador = request.user.perfilusuario 
            evento.save()
            messages.success(request, f'Evento "{evento.titulo}" criado com sucesso!')
            return redirect('index') 
    else:
        form = EventoForm()
        
    context = {'form': form}
    return render(request, 'criar_evento.html', context)


# --- INSCRIÇÃO EM EVENTOS (Requisito 3) ---

@login_required
def inscricao_evento(request, evento_id):
    """Requisito 3: Inscrição em eventos (Apenas para ALUNOS e PROFESSORES)."""
    evento = get_object_or_404(Evento, pk=evento_id)
    
    # Restrição: Apenas Alunos/Professores podem se inscrever
    if request.user.perfilusuario.perfil not in ['ALUNO', 'PROFESSOR']:
        messages.error(request, 'Seu perfil não permite inscrição em eventos.')
        return redirect('index')
        
    if evento.vagas_restantes() <= 0:
        messages.error(request, 'O evento não possui mais vagas disponíveis.')
        return redirect('index')
        
    try:
        # Vinculação do evento ao usuário (Requisito do PDF)
        evento.participantes.add(request.user)
        messages.success(request, f'Inscrição no evento "{evento.titulo}" realizada com sucesso!')
    except IntegrityError:
        messages.warning(request, 'Você já está inscrito neste evento.')
    
    return redirect('index')


# --- EMISSÃO DE CERTIFICADOS (Requisito 4) ---

@login_required
def emitir_certificado(request, evento_id, user_id):
    """Requisito 4: Emissão de certificados (Apenas para ORGANIZADORES)."""
    
    # Verifica se o usuário logado é um Organizador
    if request.user.perfilusuario.perfil != 'ORGANIZADOR':
        messages.error(request, 'Acesso negado. Apenas organizadores podem emitir certificados.')
        return redirect('index')
    
    evento = get_object_or_404(Evento, pk=evento_id)
    participante = get_object_or_404(User, pk=user_id)

    # Requisito 4: Só é possível emitir certificados para usuários inscritos.
    if participante not in evento.participantes.all():
        messages.error(request, f'{participante.username} não está inscrito no evento {evento.titulo}.')
        return redirect('index')

    try:
        # Cria o certificado
        codigo = uuid.uuid4().hex[:10].upper() # Código curto de 10 caracteres
        Certificado.objects.create(
            evento=evento,
            participante=participante,
            codigo_verificacao=codigo
        )
        messages.success(request, f'Certificado gerado para {participante.username} no evento {evento.titulo}. Código: {codigo}')
    except IntegrityError:
        messages.warning(request, f'O certificado para {participante.username} já havia sido emitido.')
    
    return redirect('index') # Redirecionar para uma página de Gerenciamento de Participantes seria ideal.