from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from os.path import join
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuslug import uuslug as slugify
from rest_framework.authtoken.models import Token

class User(AbstractUser):
	'''
		This user will include Twitter's (maybe) one and Facebook's one.
		Up to now we use the standard django user.
		In addition we have:
	'''
	avatar = models.ImageField(upload_to='avatars', blank=True)
	follows = models.ManyToManyField('self', related_name='followss', symmetrical=False, through='Fellowship')

	# @receiver(post_save)
	# def create_profile(sender, instance, created, **kwargs):
	# 	'''
	# 		Create a matching profile whenever a user object is created.
	# 	'''
	# 	if sender == get_user_model():
	# 		facebook_user = instance
	# 		profile_model = get_profile_model()
	# 		if profile_model == User and created:
	# 			profile, new = User.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)

class Fellowship(models.Model):
	from_user = models.ForeignKey(User, related_name='from')
	to_user = models.ForeignKey(User, related_name='to')

	class Meta:
		unique_together = ('from_user', 'to_user')

class Ability(models.Model):
	ELEMENTS = (
		('N', 'none'),
		('T', 'thunder'),
		('W', 'water'),
		('F', 'fire'),
		('B', 'blizzard'),
		('W', 'white magic'),
	)

	name = models.CharField(max_length=200, unique=True)
	description = models.TextField(blank=True)
	power = models.IntegerField(default=5)
	ap_required = models.IntegerField(default=1)
	requires = models.ManyToManyField('self', symmetrical=False)
	mp_required = models.IntegerField(default=0)
	element = models.CharField(max_length=1, choices=ELEMENTS, default=ELEMENTS[0][0])

	slug = models.CharField(max_length=200, unique=True)
	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name, instance=self)
			super(Ability, self).save(*args, **kwargs)

class Character(models.Model):
	'''
		The character the user will use to fight
	'''
	name = models.CharField(max_length=200, unique=True)
	level = models.IntegerField(default=1)
	exp = models.IntegerField(default=0)
	ap = models.IntegerField(default=0)
	guils = models.IntegerField(default=1000)
	#stats
	hp = models.IntegerField(default=250)
	mp = models.IntegerField(default=50)
	curr_hp = models.IntegerField(default=250)
	curr_mp = models.IntegerField(default=50)
	power = models.IntegerField(default=10)
	mpower = models.IntegerField(default=10)
	defense = models.IntegerField(default=10)
	mdefense = models.IntegerField(default=10)
	#relations
	owner = models.ForeignKey(User)
	abilities = models.ManyToManyField(Ability, through='LearntAbility')
	items = models.ManyToManyField('Item', through='InventoryRecord')
	#equip

	def get_next_abilities(self):
		abilities = list(Ability.objects.all())
		learnt_abilities = list(self.abilities.all())

		def filter_function(ability):
			if set(ability.requires.all()).issubset(learnt_abilities):
				return True
			return False

		return list(set(filter(filter_function, abilities)) - set(learnt_abilities))

	def get_defense(self):
		try:
			armor = self.items.filter(inventoryrecord__equipped=True,
										inventoryrecord__item__item_type=Item.ITEM_TYPE[2][0]).get()
			armor_def = armor.power
		except ObjectDoesNotExist:
			armor_def = 0

		return self.defense + armor_def

	def clean(self):
		if self.curr_hp > self.hp or self.curr_mp > self.mp:
			raise ValidationError('It is not possible to overcome maximum hps or mps')

class LearntAbility(models.Model):
	character = models.ForeignKey(Character)
	ability = models.ForeignKey(Ability)

	class Meta:
		unique_together = ('character', 'ability')

class InventoryRecord(models.Model):
	owner = models.ForeignKey(Character)
	item = models.ForeignKey('Item')
	quantity = models.IntegerField(default=1)
	equipped = models.BooleanField(default=False)

	class Meta:
		unique_together = ('owner', 'item')

class Mob(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.TextField(blank=True)
	weakness = models.CharField(max_length=1, choices=Ability.ELEMENTS, default=Ability.ELEMENTS[0][0])
	#stats
	level = models.IntegerField(default=1)
	hp = models.IntegerField(default=250)
	power = models.IntegerField(default=10)
	mpower = models.IntegerField(default=10)
	defense = models.IntegerField(default=10)
	mdefense = models.IntegerField(default=10)
	speed = models.IntegerField(default=10)
	guils = models.IntegerField(default=0)
	exp = models.IntegerField(default=0)
	ap = models.IntegerField(default=1)
	#relations
	drops = models.ManyToManyField('Item')
	abilities = models.ManyToManyField(Ability)

	slug = models.CharField(max_length=200, unique=True)
	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name, instance=self)
			super(Mob, self).save(*args, **kwargs)

class Room(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.TextField(blank=True)

	slug = models.CharField(max_length=200, unique=True)
	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name, instance=self)
			super(Room, self).save(*args, **kwargs)

	class Meta:
		abstract = True

class PVERoom(Room):
	mobs = models.ManyToManyField(Mob)


class RelaxRoom(Room):
	sells = models.ManyToManyField('Item')

class Item(models.Model):
	ITEM_TYPE = (
		('R', 'Restorative Item'),
		('W', 'Weapon'),
		('A', 'Armor'),
	)
	name = models.CharField(max_length=200, unique=True)
	description = models.TextField(blank=True)
	item_type = models.CharField(max_length=1, choices=ITEM_TYPE, blank=False)
	power = models.IntegerField(default=0)
	cost = models.IntegerField(default=50)

	slug = models.CharField(max_length=200, unique=True)
	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name, instance=self)
			super(Item, self).save(*args, **kwargs)

class Post(models.Model):
	content = models.TextField(max_length=1024)
	author = models.ForeignKey(User)
	room = models.ForeignKey(RelaxRoom)

class Comment(models.Model):
	content = models.TextField(max_length=1024)
	author = models.ForeignKey(User)
	post = models.ForeignKey(Post)

class Battle(models.Model):
	character = models.ForeignKey(Character)
	mob = models.ForeignKey(Mob)
	mob_hp = models.IntegerField(blank=True)

	def calculate_character_damage(self, ability):
		'''
			Algorithms taken from http://www.gamefaqs.com/ps2/459841-final-fantasy-xii/faqs/45900
			if physical:
				DMG = [ATK x RANDOM(1~1.125) - DEF] x [1 + STR x (Lv+STR)/256]
			if black:
				DMG = [POW x RANDOM(1~1.125) - MDEF] x [2 + MAG x (Lv+MAG)/256)]
			if white:
				HEAL = POW x RANDOM(1~1.125) x [2 + MAG x (Lv+MAG)/256)]
		'''
		import random
		PHYSICAL = Ability.ELEMENTS[0][0]
		WHITE = Ability.ELEMENTS[5][0]
		weapon = self.character.items.filter(inventoryrecord__equipped=True,
						inventoryrecord__item__item_type=Item.ITEM_TYPE[1][0])

		if ability.element == PHYSICAL:
			dmg = (weapon.power * random.uniform(1, 1.125) - self.mob.defense) \
					* (1 + self.character.power * (self.character.level + self.character.power) / 256)
		elif ability.element == WHITE:
			dmg = - (ability.power * random.uniform(1, 1.125)) \
				* (2 + self.character.mpower * (self.character.level + self.character.mpower) / 256)
		else:
			dmg = (ability.power * random.uniform(1, 1.125) - self.mob.mdefense) \
				* (2 + self.character.mpower * (self.character.level + self.character.mpower) / 256)

		return int(round(dmg))

	def calculate_mob_damage(self, ability):
		'''
			Algorithms taken from http://www.gamefaqs.com/ps2/459841-final-fantasy-xii/faqs/45900
			if physical:
				DMG = [ATK x RANDOM(1~1.125) - DEF] x [1 + STR x (Lv+STR)/256]
			if black:
				DMG = [POW x RANDOM(1~1.125) - MDEF] x [2 + MAG x (Lv+MAG)/256)]
			if white:
				HEAL = POW x RANDOM(1~1.125) x [2 + MAG x (Lv+MAG)/256)]
		'''
		import random
		PHYSICAL = Ability.ELEMENTS[0][0]
		WHITE = Ability.ELEMENTS[5][0]

		if ability.element == PHYSICAL:
			dmg = (self.mob.power * random.uniform(1, 1.125) - self.character.get_defense()) \
					* (1 + self.mob.power * (self.mob.level + self.mob.power) / 256)
		elif ability.element == WHITE:
			dmg = - (ability.power * random.uniform(1, 1.125)) \
				* (2 + self.mob.mpower * (self.mob.level + self.mob.mpower) / 256)
		else:
			dmg = (ability.power * random.uniform(1, 1.125) - self.character.mdefense) \
				* (2 + self.mob.mpower * (self.mob.level + self.mob.mpower) / 256)

		return int(round(dmg))

	def assign_damage_to_character(self, damage):
		self.character.curr_hp -= damage
		self.character.save()

	def assign_damage_to_mob(self, damage):
		self.mob_hp -= damage
		self.save()

