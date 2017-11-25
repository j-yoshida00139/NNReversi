from django.shortcuts import render
from django.middleware.csrf import get_token


def index(request):
	csrf_token = get_token(request)
	return render(request, 'personal/home.html')


def contact(request):
	return render(request, 'personal/basic.html', {'contents':['If you would like to contact me, please email me','bakinsley@gmail.com']})
