from django.db import models


class BestMove(models.Model):
	first_half_arrangement = models.BigIntegerField(null=False)
	last_half_arrangement = models.BigIntegerField(null=False)
	move_index = models.IntegerField(null=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ('first_half_arrangement', 'last_half_arrangement')
