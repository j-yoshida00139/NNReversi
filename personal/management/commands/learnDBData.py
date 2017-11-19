from django.core.management.base import BaseCommand
from personal.nncore import nnHandler


class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		nnHandlerIns = nnHandler.NNHandler()
		nnHandlerIns.learn()
