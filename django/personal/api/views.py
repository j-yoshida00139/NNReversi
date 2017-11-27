from rest_framework import viewsets
from .serializer import BestMoveSerializer
from ..models import BestMove


class BestMoveViewSet(viewsets.ModelViewSet):
	serializer_class = BestMoveSerializer
	queryset = BestMove.objects.all()
