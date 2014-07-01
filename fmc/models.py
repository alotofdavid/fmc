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
	def inverse(self):
		return rubik.Algorithm(self.scramble).invert()

	def rank(self):
		arr = self.submission_set.order_by('move_count')
		position_dict = {}
		curr_position = 1
		for i in range(len(arr)-1):
			position_dict[arr[i]] = curr_position
			if arr[i].move_count < arr[i+1].move_count:
				curr_position += 1
		#handle last index of array
		position_dict[arr[len(arr)-1]] = curr_position
		#TODO: store this dictionary somewhere? I believe this runs in O(n) time so not a huge priority
		for sub in arr:
			position = position_dict[sub]
			sub.ranking = position
			sub.score = 4-position if position<4 else 0
			sub.save()
	def __unicode__(self):
		return self.scramble;

	scramble = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	#end_date = timezone.now() + datetime.timedelta(days=7)

class Submission(models.Model):
	def sol_one_line(self):
		return ' '.join(self.solution.split())
	def __unicode__(self):
		return self.solution

	score = models.IntegerField()
	ranking = models.IntegerField()
	scramble = models.ForeignKey(Scramble)
	user = models.ForeignKey(User, blank=True, null=True)
	move_count = models.IntegerField()
	name = models.CharField(max_length=50)
	solution = models.TextField(max_length=500)
	comments = models.TextField(max_length=500, blank=True, null=True)
