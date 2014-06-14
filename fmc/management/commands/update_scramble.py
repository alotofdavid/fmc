from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from fmc.models import Scramble
from random import randint as r
from weekly_fmc import settings
import urllib
from django.shortcuts import get_object_or_404

class Command(BaseCommand): 
    def handle(self, *args, **options):
		s_id = args[0]
		s = get_object_or_404(Scramble, pk=s_id)                 
		url = "http://cube.crider.co.uk/visualcube.php?bg=t&fmt=png&size=150&sch=wrgyob&pzl=3&alg="+__unicode__(scramble)
		uopen = urllib.urlopen(url)
		stream = uopen.read()
		file = open('static/images/scramble'+str(s.id)+'.png','w')
		file.write(stream)
		file.close()
