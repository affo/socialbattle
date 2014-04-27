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
			lookup_field='name'
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
		fields = ('url', 'name', 'mobs', )
		lookup_field = 'name'

class RelaxRoomSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='relaxroom-detail',
			lookup_field='name',
		)

	sells = serializers.HyperlinkedRelatedField(
			view_name='item-detail',
			lookup_field='pk',
			many=True,
		) 

	class Meta:
		model = models.RelaxRoom
		fields = ('url', 'name', 'sells', )
		lookup_field = 'name'

class ItemSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Item
		fields = ('url', 'name', )

class MobSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Mob
		fields = ('url', 'name', )