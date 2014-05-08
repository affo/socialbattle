from rest_framework import serializers
from socialbattle.api import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
	password = serializers
	class Meta:
		model = models.User
		fields = ('url', 'id', 'username', 'first_name', 'last_name', 'password','email', 'follows')
		write_only_fields = ('password', )
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
			lookup_field='slug',
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

class ItemSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Item
		fields = ('url', 'name', 'cost', 'item_type')
		lookup_field = 'slug'

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

	current_weapon = serializers.HyperlinkedRelatedField(
			view_name='item-detail',
			lookup_field='slug',
		)
	current_armor = serializers.HyperlinkedRelatedField(
			view_name='item-detail',
			lookup_field='slug',
		)

	physical_abilities = serializers.HyperlinkedRelatedField(
			view_name='physicalability-detail',
			lookup_field='slug',
			many=True,
		)

	black_magic_abilities = serializers.HyperlinkedRelatedField(
			view_name='blackmagicability-detail',
			lookup_field='slug',
			many=True,
		)

	white_magic_abilities = serializers.HyperlinkedRelatedField(
			view_name='whitemagicability-detail',
			lookup_field='slug',
			many=True,
		)

	level = serializers.Field(source='level')
	guils = serializers.Field(source='guils')
	hp = serializers.Field(source='hp')
	mp = serializers.Field(source='mp')
	power = serializers.Field(source='power')
	mpower = serializers.Field(source='mpower')

	class Meta:
		model = models.Character
		fields = (
			'url', 'name', 'level', 'guils', 'owner',
			'current_weapon',
			'current_armor',
			'hp', 'mp',
			'power', 'mpower',
			'physical_abilities', 'black_magic_abilities', 'white_magic_abilities',
		)

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
		lookup_field='slug',
	)

	quantity = serializers.WritableField(source='quantity')

	class Meta:
		model = models.InventoryRecord
		fields = ('url', 'owner', 'item', 'quantity', )

class PVERoomSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='pveroom-detail',
			lookup_field='slug',
		)

	mobs = serializers.HyperlinkedRelatedField(
			view_name='mob-detail',
			lookup_field='slug',
			many=True,
		)

	class Meta:
		model = models.PVERoom
		fields = ('url', 'name', 'mobs', )


class RelaxRoomSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='relaxroom-detail',
			lookup_field='slug',
		)

	sells = serializers.HyperlinkedRelatedField(
			view_name='item-detail',
			lookup_field='slug',
			many=True,
		) 

	class Meta:
		model = models.RelaxRoom
		fields = ('url', 'name', 'sells', )

class PhysicalAbilitySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.PhysicalAbility
		fields = ('url', 'name', 'description', 'power', 'requires')
		lookup_field = 'slug'
		read_only_fields = ('name', 'description', 'power', 'requires')

class WhiteMagicAbilitySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.WhiteMagicAbility
		fields = ('url', 'name', 'description', 'power', 'requires')
		lookup_field = 'slug'

class BlackMagicAbilitySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.BlackMagicAbility
		fields = ('url', 'name', 'description', 'power', 'requires', 'element')
		lookup_field = 'slug'

class MobSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='mob-detail',
			lookup_field='slug',
		)

	drops = serializers.HyperlinkedRelatedField(
			view_name='item-detail',
			lookup_field='slug',
			many=True,
		) 

	class Meta:
		model = models.Mob
		fields = ('url', 'name', 'drops', )