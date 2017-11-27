from rest_framework import serializers
from ..models import BestMove


class BestMoveSerializer(serializers.ModelSerializer):
	class Meta:
		model = BestMove
		fields = '__all__'
