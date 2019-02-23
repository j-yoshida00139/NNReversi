from rest_framework import viewsets

from .serializer import NNMoveSerializer


# from ..models import BestMove


class NNMoveViewSet(viewsets.ModelViewSet):
    serializer_class = NNMoveSerializer
# queryset = BestMove.objects.all()
