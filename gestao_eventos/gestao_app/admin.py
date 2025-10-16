# gestao_app/admin.py

from django.contrib import admin
from .models import PerfilUsuario, Evento, Certificado
# Register your models here.

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('user', 'perfil', 'instituicao_ensino')

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'data_inicio', 'vagas_restantes')
    list_filter = ('tipo', 'data_inicio')

@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('participante', 'evento', 'codigo_verificacao', 'data_emissao')
    search_fields = ('participante__username', 'evento__titulo')