from rest_framework import serializers
import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.User
		fields = ('url', 'username', 'first_name', 'last_name', 'email', 'follows', )
		lookup_field = 'username'

class CharacterSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='character-detail',
			lookup_field='pk'
		)

	owner = serializers.HyperlinkedRelatedField(
			view_name='user-detail',
			lookup_field='username'
		)

	class Meta:
		model = models.Character
		fields = ('url', 'name', 'level', 'owner', )

class PVERoomSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.PVERoom
		fields = ('name', 'mobs', )
		lookup_field = 'name'

class RelaxRoomSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.RelaxRoom
		fields = ('name', 'sells', )
		lookup_field = 'name'

class ItemSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Item
		fields = ('url', 'name', )
		lookup_field = 'name'

class MobSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Mob
		fields = ('url', 'name', )
		lookup_field = 'name'