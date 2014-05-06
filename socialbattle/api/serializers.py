from rest_framework import serializers
from socialbattle.api import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.User
		fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email', 'follows', )
		lookup_field = 'username'

class FellowshipSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='fellowship-detail',
			lookup_field='pk',
		)

	from_user = serializers.HyperlinkedRelatedField(
			view_name='user-detail',
			lookup_field='username',
			read_only=True,
		)

	to_user = serializers.PrimaryKeyRelatedField(source='to_user')

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
			read_only=True,
		)
	room = serializers.HyperlinkedRelatedField(
			view_name='relaxroom-detail',
			lookup_field='name',
			read_only=True,
		)

	class Meta:
		model = models.Post
		fields = ('url', 'content', 'author', 'room', )

class CommentSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='comment-detail',
			lookup_field = 'pk',
		)

	post = serializers.HyperlinkedRelatedField(
			view_name='post-detail',
			lookup_field='pk',
			read_only=True,
		)

	author = serializers.HyperlinkedRelatedField(
			view_name='user-detail',
			lookup_field='username',
			read_only=True,
		)

	class Meta:
		model = models.Comment
		fields = ('url', 'content', 'author', 'post', )

class CharacterSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='character-detail',
			lookup_field='name'
		)

	owner = serializers.HyperlinkedRelatedField(
			view_name='user-detail',
			lookup_field='username',
			read_only=True,
		)

	level = serializers.Field(source='level')
	guils = serializers.Field(source='guils')

	class Meta:
		model = models.Character
		fields = ('url', 'name', 'level', 'guils', 'owner', )

class InventoryRecordSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
		view_name='inventoryrecord-detail',
		lookup_field='pk',
	)

	owner = serializers.HyperlinkedRelatedField(
		view_name='character-detail',
		lookup_field='name',
		read_only=True,
	)

	item = serializers.HyperlinkedRelatedField(
		view_name='item-detail',
		lookup_field='pk',
		read_only=True,
	)

	quantity = serializers.Field(source='quantity')

	class Meta:
		model = models.InventoryRecord
		fields = ('url', 'owner', 'item', 'quantity', )

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
		fields = ('url', 'name', 'cost', 'item_type')

class PhysicalAbilitySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.PhysicalAbility
		fields = ('url', 'name', 'description', 'power', 'requires')

class WhiteMagicAbilitySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.WhiteMagicAbility
		fields = ('url', 'name', 'description', 'power', 'requires')

class BlackMagicAbilitySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.BlackMagicAbility
		fields = ('url', 'name', 'description', 'power', 'requires', 'element')

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