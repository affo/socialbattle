from rest_framework import serializers
import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.User
		fields = ('url', 'username', 'first_name', 'last_name', 'email', 'follows', )
		lookup_field = 'username'

class FellowshipSerializer(serializers.HyperlinkedModelSerializer):
	from_user_id = serializers.HyperlinkedRelatedField(
			view_name='user-detail',
			lookup_field='username'
		)

	to_user_id = serializers.HyperlinkedRelatedField(
			view_name='user-detail',
			lookup_field='username'
		)

	class Meta:
		model = models.Fellowship
		fields = ('url', 'from_user_id', 'to_user_id')

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
	url = serializers.HyperlinkedIdentityField(
			view_name='pveroom-detail',
			lookup_field='name',
		)

	mobs = serializers.HyperlinkedRelatedField(
			view_name='mob-detail',
			lookup_field='name',
			many=True,
		)

	class Meta:
		model = models.PVERoom
		fields = ('url', 'name', 'mobs', )


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

class ItemSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Item
		fields = ('url', 'name', )

class MobSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='mob-detail',
			lookup_field='name',
		)

	drops = serializers.HyperlinkedRelatedField(
			view_name='item-detail',
			lookup_field='pk',
			many=True,
		) 

	class Meta:
		model = models.Mob
		fields = ('url', 'name', 'drops', )