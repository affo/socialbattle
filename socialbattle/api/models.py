from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from os.path import join
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from uuslug import uuslug as slugify
from rest_framework.authtoken.models import Token

import urllib, urllib2, json
from socialbattle import settings

GRAVATAR_USER_URL = 'http://www.gravatar.com/avatar/%s?d=identicon'
GRAVATAR_CHARACTER_URL = 'http://www.gravatar.com/avatar/%s?d=identicon'
GRAVATAR_MOB_URL = 'http://www.gravatar.com/avatar/%s?d=retro'

class FBObjectMixin(models.Model):
	fb_id = models.CharField(max_length=50)
	fb_object = {}
	_fb_data = {
		'access_token': settings.FACEBOOK_APP_ACCESS_TOKEN,
		'object': {},
	}

	@property
	def fb_data(self):
	    return self._fb_data

	@fb_data.setter
	def fb_data(self, value):
		#expecting value as self.fb_object
	    self._fb_data['object'] = value

	class Meta:
		abstract = True

@receiver(pre_save)
def add_to_fb_objects(sender, instance=None, **kwargs):
	return
	try:
		if not instance.fb_id:
			class_name = sender.__name__.lower()
			if class_name == 'item': class_name = 'loot' #problems with facebook types...
			url = settings.FB_OBJECTS_URL %  class_name
			print url
			instance.fb_data = instance.fb_object
			data = urllib.urlencode(instance.fb_data)
			req = urllib2.Request(url=url, data=data)
			res = urllib2.urlopen(req)
			obj = json.load(res)
			instance.fb_id = obj['id']
			print str(instance.name) + ' ---> ' + instance.fb_id
	except AttributeError:
		# it means that the attr has not .fb_id
		pass

@receiver(post_delete)
def remove_from_fb_objects(sender, instance=None, **kwargs):
	try:
		url = 'https://graph.facebook.com/%s?access_token=%s' % (instance.fb_id, settings.FACEBOOK_APP_ACCESS_TOKEN)
		req = urllib2.Request(url=url)
		req.get_method = lambda: 'DELETE'
		res = urllib2.urlopen(req)
		if res.read() == 'true':
			print 'FB deleted instance ' + instance.fb_id
	except AttributeError:
		# it means that the attr has not .fb_id
		pass
	

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


# @receiver(post_save, sender=User)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
# 	if created:
# 		Token.objects.create(user=instance)

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
		('H', 'white magic'),
		('P', 'physical'),
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
		return None

	def update_mp(self, ability):
		return None

from socialbattle.api.mechanics import BASE_STATS
from django.core import validators
from django.utils.translation import ugettext_lazy as _
class Character(TargetMixin, FBObjectMixin):
	'''
		The character the user will use to fight
	'''
	name = models.CharField(max_length=30, unique=True,
		help_text=_('Required. 30 characters or fewer. Letters, digits and '
						'@/./+/-/_ only.'),
		validators=[
			validators.RegexValidator(r'^[\w.@+-]+$', _('Enter a valid username.'), 'invalid')
		])
	level = models.IntegerField(default=1)
	exp = models.IntegerField(default=0)
	ap = models.IntegerField(default=10)
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
	inventory = models.ManyToManyField('Item', through='InventoryRecord')

	@property
	def fb_object(self):
		return {
			'title': str(self.name),
			'image': self.img,
		}

	def get_next_abilities(self):
		abilities = list(Ability.objects.all())
		learnt_abilities = list(self.abilities.all())

		def filter_function(ability):
			if set(ability.requires.all()).issubset(learnt_abilities):
				return True
			return False

		return list(set(filter(filter_function, abilities)) - set(learnt_abilities))

	def update_hp(self, damage):
		self.curr_hp -= damage
		if self.curr_hp > self.max_hp:
			self.curr_hp = self.max_hp

		if self.curr_hp < 0:
			self.curr_hp = 0
		self.save()
		return self.curr_hp

	def update_mp(self, ability):
		self.curr_mp -= ability.mp_required
		if self.curr_mp > self.max_mp:
			self.curr_mp = self.max_mp

		if self.curr_mp < 0:
			self.curr_mp = 0
		self.save()
		return self.curr_mp

	def check_exchange(self, exchange):
		try:
			record = InventoryRecord.objects.get(owner=self, item=exchange.item)
		except ObjectDoesNotExist:
			return False
		
		if exchange.quantity > record.quantity:
			return False

		return True

	def add_to_inventory(self, exchange):
		try:
			record = InventoryRecord.objects.get(owner=self, item=exchange.item)
			record.quantity += exchange.quantity
			record.save()
		except ObjectDoesNotExist:
			record = InventoryRecord.objects.create(owner=self, item=exchange.item, quantity=exchange.quantity)

	def remove_from_inventory(self, exchange):
		record = InventoryRecord.objects.get(owner=self, item=exchange.item)
		record.quantity -= exchange.quantity
		if record.quantity <= 0:
			record.delete()
		else:
			record.save()

	@property
	def weapon(self):
		try:
			weapon = InventoryRecord.objects.filter(owner=self, equipped=True,
										item__item_type=Item.ITEM_TYPE[1][0]).get()
		except ObjectDoesNotExist:
			return None

		return weapon

	@property
	def armor(self):
		try:
			armor = InventoryRecord.objects.filter(owner=self, equipped=True,
										item__item_type=Item.ITEM_TYPE[2][0]).get()
		except ObjectDoesNotExist:
			return None

		return armor

	@property
	def weapons(self):
		try:
			weapons = InventoryRecord.objects.filter(owner=self, item__item_type=Item.ITEM_TYPE[1][0]).all()
		except ObjectDoesNotExist:
			return None
		return weapons

	@property
	def armors(self):
		try:
			armors = InventoryRecord.objects.filter(owner=self, item__item_type=Item.ITEM_TYPE[2][0]).all()
		except ObjectDoesNotExist:
			return None
		return armors

	@property
	def items(self):
		try:
			items = InventoryRecord.objects.filter(owner=self, item__item_type=Item.ITEM_TYPE[0][0]).all()
		except ObjectDoesNotExist:
			return None
		return items
	

	@property
	def defense(self):
		if self.armor:
			return self.armor.item.power
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
		if self.weapon:
			return self.weapon.item.power
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

class Mob(FBObjectMixin, TargetMixin):
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
	def fb_object(self):
		return {
			'title': str(self.name),
			'image': self.img,
			'description': str(self.description),
		}

	@property
	def curr_mp(self):
	    return self.mp

	@property
	def weapon(self):
		return None

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

class Room(FBObjectMixin):
	name = models.CharField(max_length=200, unique=True)
	description = models.TextField(blank=True)

	slug = models.CharField(max_length=200, unique=True)

	@property
	def img(self):
		import hashlib
		ash = hashlib.md5(self.slug.strip().lower()).hexdigest()
		return GRAVATAR_USER_URL % ash

	@property
	def fb_object(self):
		return {
			'title': str(self.name),
			'image': self.img,
			'description': str(self.description),
		}

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

class Item(FBObjectMixin):
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

	@property
	def img(self):
		import hashlib
		ash = hashlib.md5(self.slug.strip().lower()).hexdigest()
		return GRAVATAR_USER_URL % ash

	@property
	def fb_object(self):
		return {
			'title': str(self.name),
			'image': self.img,
			'description': str(self.description),
		}

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

	@property
	def no_comments(self):
		return self.comment_set.count();


	#exchange
	character = models.ForeignKey(Character, null=True)

	@property
	def exchanged_items(self):
		try:
			return ExchangeRecord.objects.filter(post=self).all()
		except ObjectDoesNotExist:
			return []
	
	give_guils = models.IntegerField(default=0)
	receive_guils = models.IntegerField(default=0)

	opened = models.BooleanField(default=True)

	# def clean(self):
	# 	give_not_receive = (self.give_items or self.give_guils) and not (self.receive_items or self.receive_guils)
	# 	receive_not_give = not (self.give_items or self.give_guils) and (self.receive_items or self.receive_guils)
	# 	if give_not_receive or receive_not_give:
	# 		raise ValidationError('It is not possible to give or receive for nothing')

class ExchangeRecord(models.Model):
	post = models.ForeignKey(Post)
	item = models.ForeignKey(Item)
	quantity = models.IntegerField(default=1)
	given = models.BooleanField(default=True)

class Comment(models.Model):
	content = models.TextField(max_length=1024)
	author = models.ForeignKey(User)
	post = models.ForeignKey(Post)
	time = models.DateTimeField(auto_now=True)

