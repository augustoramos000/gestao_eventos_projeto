from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Novas importações para a geração de PDF
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io

from .models import Evento, Inscricao, Usuario
from .forms import UserCreationForm, LoginForm, EventoForm

# --- Views existentes (sem alteração) ---
def listar_eventos(request):
    eventos = Evento.objects.all().order_by('data_inicio')
    eventos_inscritos_ids = []
    if request.user.is_authenticated:
        eventos_inscritos_ids = Inscricao.objects.filter(usuario=request.user).values_list('evento_id', flat=True)
    contexto = { 'eventos': eventos, 'eventos_inscritos_ids': list(eventos_inscritos_ids) }
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
        form = EventoForm()
    return render(request, 'gestao_app/criar_evento.html', {'form': form})

# --- NOVAS VIEWS PARA CERTIFICADOS ---

@login_required
def detalhe_certificado(request, inscricao_id):
    """
    Mostra uma página com os detalhes do certificado e um botão para download.
    """
    inscricao = get_object_or_404(Inscricao, id=inscricao_id, usuario=request.user)
    return render(request, 'gestao_app/detalhe_certificado.html', {'inscricao': inscricao})

@login_required
def gerar_pdf_certificado(request, inscricao_id):
    """
    Gera o ficheiro PDF do certificado e o entrega para download.
    """
    inscricao = get_object_or_404(Inscricao, id=inscricao_id, usuario=request.user)

    # Cria um buffer de memória para o PDF
    buffer = io.BytesIO()

    # Cria o objeto PDF, usando o buffer como o seu "ficheiro"
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- Desenha o conteúdo do PDF ---
    p.setTitle(f"Certificado - {inscricao.evento.nome}")

    # Título do Certificado
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(width / 2.0, height - 2 * inch, "Certificado de Participação")

    # Texto principal
    p.setFont("Helvetica", 12)
    texto = p.beginText(1.5 * inch, height - 3.5 * inch)
    texto.setFont("Helvetica", 12)
    texto.textLine("Certificamos que")
    texto.moveCursor(0, 0.5*inch) # Espaçamento
    texto.setFont("Helvetica-Bold", 14)
    texto.textLine(f"{inscricao.usuario.get_full_name()}")
    texto.moveCursor(0, 0.5*inch) # Espaçamento
    texto.setFont("Helvetica", 12)
    texto.textLine(f"participou no evento \"{inscricao.evento.nome}\",")
    texto.textLine(f"realizado em {inscricao.evento.data_inicio.strftime('%d/%m/%Y')},")
    texto.textLine(f"organizado por {inscricao.evento.organizador_responsavel.get_full_name()}.")
    p.drawText(texto)

    # Assinatura (exemplo)
    p.line(3 * inch, 2.5 * inch, 5.5 * inch, 2.5 * inch)
    p.drawCentredString(4.25 * inch, 2.25 * inch, "Assinatura do Organizador")

    # --- Finaliza o PDF ---
    p.showPage()
    p.save()

    # Retorna o buffer para o início
    buffer.seek(0)
    
    # Cria a resposta HTTP com o tipo de conteúdo correto para PDF
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificado_{inscricao.evento.nome}.pdf"'
    
    return response

