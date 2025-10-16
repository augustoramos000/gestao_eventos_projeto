# gestao_app/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PerfilUsuario(models.Model):
    """Estende o usuário padrão do Django para adicionar campos específicos."""
    
    # Mantenha o PERFIL_CHOICES DENTRO da classe
    PERFIL_CHOICES = [
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('ORGANIZADOR', 'Organizador'),
    ]
    
    # Vincula ao usuário de login e senha do Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Requisitos do PDF
    telefone = models.CharField(max_length=15, blank=True, null=True)
    instituicao_ensino = models.CharField(
        max_length=100, 
        help_text="Obrigatório para alunos e professores", 
        blank=True, 
        null=True
    )
    # Referência correta: PerfilUsuario.PERFIL_CHOICES
    perfil = models.CharField(max_length=20, choices=PERFIL_CHOICES, default='ALUNO')

    def __str__(self):
        return self.user.username



class Evento(models.Model):
    """Modelo para gerenciamento de eventos."""
    
    
    TIPO_EVENTO_CHOICES = [
        ('SEMINARIO', 'Seminário'),
        ('PALESTRA', 'Palestra'),
        ('MINICURSO', 'Minicurso'),
        ('SEMANA_ACADEMICA', 'Semana Acadêmica'),
        ('OUTRO', 'Outro'),
    ]
    
    # Requisitos do PDF
    titulo = models.CharField(max_length=200)
    
    tipo = models.CharField(max_length=20, choices=TIPO_EVENTO_CHOICES) 
    data_inicio = models.DateTimeField(help_text="Data e horário inicial")
    data_fim = models.DateTimeField(help_text="Data e horário final")
    local = models.CharField(max_length=200)
    quantidade_participantes = models.IntegerField(default=0, help_text="Limite de vagas")
    
    # Organizador Responsável
    organizador = models.ForeignKey(
        'PerfilUsuario', 
        on_delete=models.SET_NULL, 
        null=True, 
        limit_choices_to={'perfil': 'ORGANIZADOR'}
    )

    # Requisito: Inscrição em eventos
    participantes = models.ManyToManyField(User, related_name='eventos_inscritos', blank=True)

    def vagas_restantes(self):
        return self.quantidade_participantes - self.participantes.count()

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ['data_inicio']


class Certificado(models.Model):
    """Modelo para a emissão de certificados (Requisito 4 do PDF)."""
    
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    participante = models.ForeignKey(User, on_delete=models.CASCADE)
    codigo_verificacao = models.CharField(max_length=50, unique=True)
    data_emissao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Certificado para {self.participante.username} - {self.evento.titulo}"
    
    class Meta:
        # Garante que um usuário só tenha um certificado por evento
        unique_together = ('evento', 'participante')