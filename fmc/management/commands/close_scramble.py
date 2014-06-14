from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from fmc.models import Scramble
from random import randint as r
from django.shortcuts import get_object_or_404

class Command(BaseCommand): 
    def handle(self, *args, **options):
		if len(args)>0:
			s = get_object_or_404(Scramble, pk=args[0])
		else:
			s = Scramble.objects.all().order_by('-pub_date')[0]
		s.rank()
