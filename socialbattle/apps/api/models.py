from django.db import models
from os.path import join
from socialbattle.settings import MEDIA_ROOT

class User(models.Model):
	'''
		This user will include Twitter's one and Facebook's one.
		In addition we have:
	'''
	username = models.CharField(max_length=200)
	email = models.EmailField()
	avatar = models.ImageField(upload_to=join(MEDIA_ROOT, 'avatars'))
	#relations
	follows = models.ManyToManyField('self', symmetrical=False) #maybe smarter than 'followed_by'

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
	user = models.ForeignKey(User)
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
	owner = models.ForeignKey(Character)


class Comment(models.Model):
	content = models.CharField(max_length=1024)
	owner = models.ForeignKey(Character)
	post = models.ForeignKey(Post)
