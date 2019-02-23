from django.middleware.csrf import get_token
from django.shortcuts import render


def index(request):
    csrf_token = get_token(request)
    return render(request, 'personal/home.html')
