from django.db import models
from django.utils import timezone
import rubik
import datetime
from django.contrib.auth.models import User

class Scramble(models.Model):
	def current(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=7)
	def end_date(self):
		return self.pub_date + datetime.timedelta(days=7)
	def __unicode__(self):
		return self.scramble;
	scramble = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	#end_date = timezone.now() + datetime.timedelta(days=7)

class Submission(models.Model):
	def __unicode__(self):
		return self.solution
	scramble = models.ForeignKey(Scramble)
	user = models.ForeignKey(User, blank=True)
	move_count = models.IntegerField()
	name = models.CharField(max_length=50)
	solution = models.TextField(max_length=500)
	comments = models.TextField(max_length=500, blank=True)