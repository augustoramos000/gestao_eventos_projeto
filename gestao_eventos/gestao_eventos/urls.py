# gestao_eventos/gestao_eventos/urls.py (Arquivo de rotas do projeto principal)

from django.contrib import admin
from django.urls import path, include # <--- Importe 'include'

urlpatterns = [
    # 1. Rota de administração
    path('admin/', admin.site.urls),
    
    # 2. Rota principal: Inclui todas as rotas da sua aplicação 'gestao_app'
    path('', include('gestao_app.urls')), 
]