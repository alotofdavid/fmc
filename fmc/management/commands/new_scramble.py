from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from fmc.models import Scramble
from random import randint as r
class Command(BaseCommand): 
    def handle(self, *args, **options):
	scramble = ""
	m=b=9
	for u in range(20):
		c=b;b=m
		while c+b-4 and m==c or m==b:
			m=r(0,5)
		scramble += "URFBLD"[m]+" '2"[r(0,2)]+" "
	scramble = scramble.replace("  "," ")[:-1]
	s = Scramble(scramble=scramble, pub_date=timezone.now())
	s.save()
