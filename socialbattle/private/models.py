from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from os.path import join
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from uuslug import uuslug as slugify
from rest_framework.authtoken.models import Token

GRAVATAR_USER_URL = 'http://www.gravatar.com/avatar/%s?d=identicon'
GRAVATAR_CHARACTER_URL = 'http://www.gravatar.com/avatar/%s?d=identicon'
GRAVATAR_MOB_URL = 'http://www.gravatar.com/avatar/%s?d=retro'

class User(AbstractUser):
	'''
		This user will include Twitter's (maybe) one and Facebook's one.
		Up to now we use the standard django user.
		In addition we have:
	'''
	follows = models.ManyToManyField('self', related_name='followss', symmetrical=False, through='Fellowship')
	img = models.URLField()

	@property
	def no_following(self):
		return self.follows.count();

	@property
	def no_followers(self):
		return self.followss.count();


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)

@receiver(post_save, sender=User)
def add_image_url(sender, instance=None, created=False, **kwargs):
	if created:
		import hashlib
		ash = hashlib.md5(instance.email.strip().lower()).hexdigest()
		instance.img = GRAVATAR_USER_URL % ash
		instance.save()
		

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
	ctf = models.IntegerField(default=30)

	slug = models.CharField(max_length=200, unique=True)
	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name, instance=self)
			super(Ability, self).save(*args, **kwargs)

class TargetMixin(object):
	def update_hp(self, damage):
		pass

	def update_mp(self, ability):
		pass

from socialbattle.private.mechanics import BASE_STATS
class Character(models.Model, TargetMixin):
	'''
		The character the user will use to fight
	'''
	name = models.CharField(max_length=200, unique=True)
	level = models.IntegerField(default=1)
	exp = models.IntegerField(default=0)
	ap = models.IntegerField(default=0)
	guils = models.IntegerField(default=1000)
	#stats
	max_hp = models.IntegerField(default=BASE_STATS['HP'][0])
	max_mp = models.IntegerField(default=BASE_STATS['MP'][0])
	curr_hp = models.IntegerField(default=BASE_STATS['HP'][0])
	curr_mp = models.IntegerField(default=BASE_STATS['MP'][0])
	stre = models.IntegerField(default=BASE_STATS['STR'][0])
	mag = models.IntegerField(default=BASE_STATS['MAG'][0])
	vit = models.IntegerField(default=BASE_STATS['VIT'][0])
	spd = models.IntegerField(default=BASE_STATS['SPD'][0])
	#relations
	owner = models.ForeignKey(User)
	abilities = models.ManyToManyField(Ability, through='LearntAbility')
	items = models.ManyToManyField('Item', through='InventoryRecord')

	def get_next_abilities(self):
		abilities = list(Ability.objects.all())
		learnt_abilities = list(self.abilities.all())

		def filter_function(ability):
			if set(ability.requires.all()).issubset(learnt_abilities):
				return True
			return False

		return list(set(filter(filter_function, abilities)) - set(learnt_abilities))

	def get_weapon(self):
		try:
			weapon = self.items.filter(inventoryrecord__equipped=True,
										inventoryrecord__item__item_type=Item.ITEM_TYPE[1][0]).get()
		except ObjectDoesNotExist:
			return None

		return weapon


	def get_armor(self):
		try:
			armor = self.items.filter(inventoryrecord__equipped=True,
										inventoryrecord__item__item_type=Item.ITEM_TYPE[2][0]).get()
		except ObjectDoesNotExist:
			return None

		return armor

	def update_hp(self, damage):
		self.curr_hp -= damage
		if self.curr_hp > self.max_hp:
			self.curr_hp = self.max_hp

		if self.curr_hp < 0:
			self.curr_hp = 0
		self.save()

	def update_mp(self, ability):
		self.curr_mp -= ability.mp_required
		if self.curr_mp > self.max_mp:
			self.curr_mp = self.max_mp

		if self.curr_mp < 0:
			self.curr_mp = 0
		self.save()

	@property
	def defense(self):
		armor = self.get_armor()
		if armor:
			return armor.power
		else:
			return 0

	@property
	def mdefense(self):
		'''
			Should be implemented with a real magical defense.
			In the future, with more work on equipments...
		'''
		return 0

	@property
	def atk(self):
		weapon = self.get_weapon()
		if weapon:
			return weapon.power
		else:
			return 11 #as ffxii does

	@property
	def img(self):
		import hashlib
		ash = hashlib.md5(self.name.strip().lower()).hexdigest()
		return GRAVATAR_CHARACTER_URL % ash

	def clean(self):
		if self.curr_hp > self.max_hp or self.curr_mp > self.max_mp:
			raise ValidationError('It is not possible to overcome maximum hps or mps')

class Mob(models.Model, TargetMixin):
	name = models.CharField(max_length=200, unique=True)
	description = models.TextField(blank=True)
	weakness = models.CharField(max_length=1, choices=Ability.ELEMENTS, default=Ability.ELEMENTS[0][0])
	#stats
	level = models.IntegerField(default=1)
	hp = models.IntegerField(default=250)
	mp = models.IntegerField(default=250)
	stre = models.IntegerField(default=10)
	mag = models.IntegerField(default=10)
	defense = models.IntegerField(default=10)
	mdefense = models.IntegerField(default=10)
	vit = models.IntegerField(default=10)
	atk = models.IntegerField(default=10)
	spd = models.IntegerField(default=10)
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

	@property
	def curr_mp(self):
	    return self.mp

	@property
	def img(self):
		import hashlib
		ash = hashlib.md5(self.slug.strip().lower()).hexdigest()
		return GRAVATAR_MOB_URL % ash
	

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
	power = models.IntegerField(default=0) #percentage of hp restored in the case of R
	cost = models.IntegerField(default=50)
	ctf = models.IntegerField(default=0)

	slug = models.CharField(max_length=200, unique=True)
	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name, instance=self)
			super(Item, self).save(*args, **kwargs)

	def get_restorative_effect(self, character):
		if self.item_type == self.ITEM_TYPE[0][0]:
			hp = character.max_hp
			hp_gain = hp * self.power / 100
		else:
			hp_gain = 0
		return int(round(hp_gain))

class Post(models.Model):
	content = models.TextField(max_length=1024)
	author = models.ForeignKey(User)
	room = models.ForeignKey(RelaxRoom)
	time = models.DateTimeField(auto_now=True)

class Comment(models.Model):
	content = models.TextField(max_length=1024)
	author = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	time = models.DateTimeField(auto_now=True)

