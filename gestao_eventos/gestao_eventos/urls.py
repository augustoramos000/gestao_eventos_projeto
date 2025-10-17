from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Inclui todas as URLs do ficheiro gestao_app/urls.py
    path('', include('gestao_app.urls')), 
]
