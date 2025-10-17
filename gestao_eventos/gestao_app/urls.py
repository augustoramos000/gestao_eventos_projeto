from django.urls import path
from . import views

urlpatterns = [
    # URLs principais e de autenticação
    path('', views.listar_eventos, name='listar_eventos'),
    path('cadastro/', views.cadastro_usuario, name='cadastrar_usuario'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),

    # URLs de eventos e inscrições
    path('minhas-inscricoes/', views.minhas_inscricoes, name='minhas_inscricoes'),
    path('evento/<int:evento_id>/inscrever/', views.inscrever_evento, name='inscrever_evento'),
    path('evento/criar/', views.criar_evento, name='criar_evento'),
    
    # URLs para certificados
    path('certificado/<int:inscricao_id>/', views.detalhe_certificado, name='detalhe_certificado'),
    path('certificado/<int:inscricao_id>/gerar-pdf/', views.gerar_pdf_certificado, name='gerar_pdf_certificado'),

    # URLs para gestão do organizador
    path('meus-eventos/', views.meus_eventos, name='meus_eventos'),
    path('evento/<int:evento_id>/gerenciar/', views.gerenciar_evento, name='gerenciar_evento'),
]

