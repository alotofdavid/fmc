from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from fmc.models import Scramble
from random import randint as r
from django.shortcuts import get_object_or_404

class Command(BaseCommand): 
    def handle(self, *args, **options):
		s = get_object_or_404(Scramble, pk=args[0])
		s.rank()
