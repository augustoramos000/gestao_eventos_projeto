from django.urls import path
from . import views

urlpatterns = [
    # Caminho para a página principal que lista os eventos
    path('', views.listar_eventos, name='listar_eventos'),

    # Caminhos para autenticação
    # CORREÇÃO: O nome da URL foi alterado para corresponder ao template.
    path('cadastro/', views.cadastro_usuario, name='cadastrar_usuario'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),

    # Caminhos para funcionalidades do usuário
    path('minhas-inscricoes/', views.minhas_inscricoes, name='minhas_inscricoes'),
    path('evento/<int:evento_id>/inscrever/', views.inscrever_evento, name='inscrever_evento'),

    # Caminhos para funcionalidades do organizador (ainda por implementar)
    path('evento/criar/', views.criar_evento, name='criar_evento'),
    path('certificado/<int:inscricao_id>/emitir/', views.emitir_certificado, name='emitir_certificado'),
]

