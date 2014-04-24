from django.db import models
from os.path import join
from django.contrib.auth.models import AbstractUser
#from django_facebook.models import FacebookModel
#from django.dispatch.dispatcher import receiver
#from django.db.models.signals import post_save
#from django_facebook.utils import get_user_model, get_profile_model

#class User(FacebookModel):
class User(AbstractUser):
	'''
		This user will include Twitter's (maybe) one and Facebook's one.
		Up to now we use the standard django user.
		In addition we have:
	'''
	#facebook_user = models.OneToOneField(settings.AUTH_USER_MODEL)
	avatar = models.ImageField(upload_to='avatars', blank=True)
	#relations
	follows = models.ManyToManyField('self', related_name='followss', symmetrical=False) #maybe smarter than 'followed_by'

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

class Character(models.Model):
	'''
		The character the user will use to fight
	'''
	name = models.CharField(max_length=200, primary_key=True) #the character has to have a unique name
	level = models.IntegerField(default=1)
	exp = models.IntegerField(default=0)
	#stats
	hp = models.IntegerField(default=250)
	mp = models.IntegerField(default=50)
	power = models.IntegerField(default=10)
	mpower = models.IntegerField(default=10)
	speed = models.IntegerField(default=10)
	#relations
	owner = models.ForeignKey(User)
	abilities = models.ManyToManyField('Ability')
	items = models.ManyToManyField('Item')

class Ability(models.Model):
	name = models.CharField(max_length=200)


class Mob(models.Model):
	name = models.CharField(max_length=200)
	#stats
	hp = models.IntegerField()
	power = models.IntegerField()
	mpower = models.IntegerField()
	guils = models.IntegerField()
	exp = models.IntegerField()
	#relations
	drops = models.ManyToManyField('Item')

class Room(models.Model):
	name = models.CharField(max_length=200)

	class Meta:
		abstract = True

class PVERoom(Room):
	mobs = models.ManyToManyField(Mob)


class RelaxRoom(Room):
	sells = models.ManyToManyField('Item')

class Item(models.Model):
	name = models.CharField(max_length=200)

class Post(models.Model):
	content = models.CharField(max_length=1024)
	author = models.ForeignKey(Character)


class Comment(models.Model):
	content = models.CharField(max_length=1024)
	author = models.ForeignKey(Character)
	post = models.ForeignKey(Post)