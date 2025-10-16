# gestao_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Rotas de Navegação
    path('', views.index, name='index'), 
    
    # Rotas de Autenticação
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),

    # Rotas de Eventos (Requisito 2 e 3)
    path('eventos/novo/', views.criar_evento, name='criar_evento'),
    path('evento/<int:evento_id>/inscrever/', views.inscricao_evento, name='inscricao_evento'),
    
    # Rotas de Certificados (Requisito 4)
    # user_id é o ID do participante para quem o certificado será emitido
    path('certificados/emitir/<int:evento_id>/<int:user_id>/', views.emitir_certificado, name='emitir_certificado'),
]