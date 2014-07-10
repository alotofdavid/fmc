from django.test import TestCase
from fmc.models import Scramble, Submission
from django.utils import timezone
from rubik import *

class ScrambleTestCase(TestCase):
	def setUp(self):
		Scramble.objects.create(scramble="R U R' U'", pub_date=timezone.now())

	def test_algorithms(self):
		"""Tests algorithm creation and inversion. """
		s = Scramble.objects.get(scramble="R U R' U'")
		self.assertTrue(valid_alg(s.scramble))
		a = Algorithm(s.scramble)
		c = Cube()
		c.apply_alg(a)
		c.apply_alg(a.invert())
		self.assertTrue(c.solved())
