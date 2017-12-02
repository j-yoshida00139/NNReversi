from django.shortcuts import render
from django.middleware.csrf import get_token


def index(request):
	csrf_token = get_token(request)
	return render(request, 'personal/home.html')
