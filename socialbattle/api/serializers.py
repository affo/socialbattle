from rest_framework import serializers
import models
import fields

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.User
		fields = ('url', 'username', 'first_name', 'last_name', 'email', 'follows', )
		lookup_field = 'username'

class FellowshipSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='fellowship-detail',
			lookup_field='pk',
		)

	from_user = serializers.HyperlinkedRelatedField(
			view_name='user-detail',
			lookup_field='username',
			many=False,
		)

	to_user = serializers.HyperlinkedRelatedField(
			view_name='user-detail',
			lookup_field='username',
			many=False,
		)

	class Meta:
		model = models.Fellowship
		fields = ('url', 'from_user', 'to_user')

class PostSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='post-detail',
			lookup_field='pk',
		)

	author = serializers.HyperlinkedRelatedField(
			view_name='user-detail',
			lookup_field='username',
			many=False,
		)

	room = serializers.HyperlinkedRelatedField(
			view_name='relaxroom-detail',
			lookup_field='name',
			many=False,
		)

	class Meta:
		model = models.Post
		fields = ('url', 'content', 'author', 'room')

class CharacterSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='character-detail',
			lookup_field='character_name'
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


#from socialbattle.api.serializers import FellowshipSerializer; from socialbattle.api.models import Fellowship; f = Fellowship.objects.get(pk=2); serializer = FellowshipSerializer(f)