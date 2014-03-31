from django.db import models
from django.utils import timezone
import rubik
import datetime

class Scramble(models.Model):
	def current(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=7)
	def __unicode__(self):
		return self.scramble;
	scramble = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	#end_date = timezone.now() + datetime.timedelta(days=7)

class Submission(models.Model):
	def __unicode__(self):
		return self.solution
	scramble = models.ForeignKey(Scramble)
	move_count = models.IntegerField()
	name = models.CharField(max_length=50)
	solution = models.CharField(max_length=400)
	comments = models.CharField(max_length=400)