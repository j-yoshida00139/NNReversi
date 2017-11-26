from django.shortcuts import render
from django.middleware.csrf import get_token
from rest_framework import viewsets
from .serializer import BestMoveSerializer
from .models import BestMove


class BestMoveViewSet(viewsets.ModelViewSet):
	serializer_class = BestMoveSerializer
	queryset = BestMove.objects.all()


def index(request):
	# csrf_token = get_token(request)
	return render(request, 'personal/home.html')
