# fake models to serialize, real models are in socialbattle.private.models
from django.db import models
from socialbattle.private.models import Ability

class Target(models.Model):
	atk = models.IntegerField(default=0)
	stre = models.IntegerField(default=0)
	mag = models.IntegerField(default=0)
	defense = models.IntegerField(default=0)
	mdefense = models.IntegerField(default=0)
	level = models.IntegerField(default=0)

class Ability(models.Model):
	power = models.IntegerField(default=0)
	element = models.CharField(
			max_length=1,
			choices=Ability.ELEMENTS,
			default=Ability.ELEMENTS[0][0],
	)

class Attack(models.Model):
	attacker = models.ForeignKey(Target)
	attacked = models.ForeignKey(Target)
	ability = models.ForeignKey(Ability)

class Ct(object):
	def __init__(self, spd, ctf):
		self.spd = spd
		self.ctf = ctf

class Stat(object):
	def __init__(self, lvl, stat):
		self.lvl = lvl
		self.stat = stat