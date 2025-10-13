# gestao_app/views.py

from django.shortcuts import render

def index(request):
    # CORREÇÃO: Mude a chamada para 'index.html'
    return render(request, 'index.html', {})