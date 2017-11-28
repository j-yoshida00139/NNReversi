from django.db import models
from django.conf import settings


class NNModel(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	accuracy_train = models.PositiveIntegerField(null=False, default=0)
	accuracy_test = models.PositiveIntegerField(null=False, default=0)
	title = models.TextField(null=False, default='')
	description = models.TextField(null=False, default='')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
