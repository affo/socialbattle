from rest_framework import serializers
import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.User
		fields = ('url', 'username', 'first_name', 'last_name', 'email', 'follows', )
		lookup_field = 'username'

class CharacterSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Character
		fields = ('url', 'name', 'level', )

class PVERoomSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.PVERoom
		fields = ('name', )

class RelaxRoomSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.RelaxRoom
		fields = ('name', )