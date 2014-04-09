from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Word(models.Model):
	word = models.CharField(max_length = 200)
	owner = models.ForeignKey('auth.User', related_name='words')

	def __unicode__(self):
		return self.word