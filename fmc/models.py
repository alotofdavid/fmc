from django.db import models
from django.utils import timezone

import datetime

class Scramble(models.Model):
	def current(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=7)
	def __unicode__(self):
		return self.scramble;
	end_date = timezone.now() + datetime.timedelta(days=7)
	scramble = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

class Submission(models.Model):
	def __unicode__(self):
		return self.solution
	comments = models.CharField(max_length=400)
	scramble = models.ForeignKey(Scramble)
	solution = models.CharField(max_length=400)
	name = models.CharField(max_length=50)