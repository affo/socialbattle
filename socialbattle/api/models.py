from django.db import models
from django.core.exceptions import ValidationError
from os.path import join
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
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

class Character(models.Model):
	'''
		The character the user will use to fight
	'''
	name = models.CharField(max_length=200, unique=True) #the character has to have a unique name
	level = models.IntegerField(default=1)
	exp = models.IntegerField(default=0)
	ap = models.IntegerField(default=0)
	guils = models.IntegerField(default=1000)
	#stats
	hp = models.IntegerField(default=250)
	mp = models.IntegerField(default=50)
	power = models.IntegerField(default=10)
	mpower = models.IntegerField(default=10)
	#relations
	owner = models.ForeignKey(User)
	#abilities
	physical_abilities = models.ManyToManyField('PhysicalAbility')
	white_magic_abilities = models.ManyToManyField('WhiteMagicAbility')
	black_magic_abilities = models.ManyToManyField('BlackMagicAbility')
	items = models.ManyToManyField('Item', through='InventoryRecord')
	#equip
	current_weapon = models.ForeignKey('Item', related_name='weapon', null=True)
	current_armor = models.ForeignKey('Item', related_name='armor', null=True)

	def clean(self):
		if self.current_armor and self.current_weapon:
			if self.current_weapon.item_type != 'W' or self.current_armor.item_type != 'A':
				raise ValidationError('The equipment is not coherent!')

class InventoryRecord(models.Model):
	owner = models.ForeignKey(Character)
	item = models.ForeignKey('Item')
	quantity = models.IntegerField(default=1)

	class Meta:
		unique_together = ('owner', 'item')


class Ability(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.TextField(blank=True)
	power = models.IntegerField(default=0)
	ap_required = models.IntegerField(default=1)
	requires = models.ManyToManyField('self', symmetrical=False)

	class Meta:
		abstract = True

class PhysicalAbility(Ability):
	pass

class MagicAbility(Ability):
	mp_required = models.IntegerField(default=1)

	class Meta:
		abstract = True

class WhiteMagicAbility(MagicAbility):
	pass

class BlackMagicAbility(MagicAbility):
	ELEMENTS = (
		('T', 'thunder'),
		('W', 'water'),
		('F', 'fire'),
		('B', 'blizzard'),
	)
	element = models.CharField(max_length=1, choices=ELEMENTS, blank=True)

class Mob(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.TextField(blank=True)
	weakness = models.CharField(max_length=1, choices=BlackMagicAbility.ELEMENTS, blank=True)
	#stats
	hp = models.IntegerField(default=250)
	power = models.IntegerField(default=10)
	guils = models.IntegerField(default=0)
	exp = models.IntegerField(default=0)
	ap = models.IntegerField(default=1)
	#relations
	drops = models.ManyToManyField('Item')

class Room(models.Model):
	name = models.CharField(max_length=200, unique=True)
	description = models.TextField(blank=True)

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
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	item_type = models.CharField(max_length=1, choices=ITEM_TYPE, blank=False)
	power = models.IntegerField(default=0)
	cost = models.IntegerField(default=50)

class Post(models.Model):
	content = models.TextField(max_length=1024)
	author = models.ForeignKey(User)
	room = models.ForeignKey(RelaxRoom)

class Comment(models.Model):
	content = models.TextField(max_length=1024)
	author = models.ForeignKey(User)
	post = models.ForeignKey(Post)
