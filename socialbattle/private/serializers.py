from rest_framework import serializers
from socialbattle.private import models

#taken from DRF
class DynamicHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
	"""
	A ModelSerializer that takes an additional `fields` argument that
	controls which fields should be displayed.
	"""

	def __init__(self, *args, **kwargs):
		# Don't pass the 'fields' arg up to the superclass
		fields = kwargs.pop('fields', None)

		# Instantiate the superclass normally
		super(DynamicHyperlinkedModelSerializer, self).__init__(*args, **kwargs)

		if fields:
			# Drop any fields that are not specified in the `fields` argument.
			allowed = set(fields)
			existing = set(self.fields.keys())
			for field_name in existing - allowed:
				self.fields.pop(field_name)

class UserSerializer(DynamicHyperlinkedModelSerializer):
	no_following = serializers.Field(source='no_following')	
	no_followers = serializers.Field(source='no_followers')

	class Meta:
		model = models.User
		fields = ('url', 'id', 'username', 'first_name', 'last_name', 'password','email', 'img',
					'no_following', 'no_followers', )
		write_only_fields = ('password', )
		read_only_fields = ('img', )
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

	to_user = serializers.HyperlinkedRelatedField(
			view_name='user-detail',
			lookup_field='username',
		)

	class Meta:
		model = models.Fellowship
		fields = ('url', 'from_user', 'to_user')

class RelaxRoomSerializer(DynamicHyperlinkedModelSerializer):
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
		fields = ('url', 'name', 'slug', 'sells', )

class PostSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='post-detail',
			lookup_field='pk',
		)

	author = UserSerializer(fields=['url', 'username', 'img'], read_only=True)

	room = RelaxRoomSerializer(fields=['url', 'name'], read_only=True)

	class Meta:
		model = models.Post
		fields = ('url', 'content', 'author', 'room', 'time' )
		read_only_fields = ('time', )

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

	author = UserSerializer(fields=['url', 'username', 'img'], read_only=True)

	class Meta:
		model = models.Comment
		fields = ('url', 'content', 'author', 'post', 'time', )

class ItemSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Item
		fields = ('url', 'name', 'cost', 'item_type', 'power', 'description')
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

	abilities = serializers.HyperlinkedRelatedField(
			view_name='ability-detail',
			lookup_field='slug',
			many=True,
			read_only=True,
		)

	img = serializers.Field(source='img')

	class Meta:
		model = models.Character
		fields = (
			'url', 'name', 'level', 'guils', 'owner',
			'ap', 'max_hp', 'max_mp', 'curr_hp', 'curr_mp',
			'stre', 'vit', 'mag', 'spd',
			'abilities', 'img', 
		)

		read_only_fields = ('level', 'ap', 'guils', 'max_hp', 'max_mp', 'stre', 'vit', 'mag', 'spd',
							'curr_hp', 'curr_mp', )

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
		read_only = True
	)

	quantity = serializers.Field(source='quantity')
	equipped = serializers.BooleanField(source='equipped')

	class Meta:
		model = models.InventoryRecord
		fields = ('url', 'owner', 'item', 'quantity', 'equipped', )

class InventoryRecordGetSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
		view_name='inventoryrecord-detail',
		lookup_field='pk',
	)

	owner = serializers.HyperlinkedRelatedField(
		view_name='character-detail',
		lookup_field='name',
		read_only=True,
	)

	item = ItemSerializer()

	quantity = serializers.Field(source='quantity')
	equipped = serializers.BooleanField(source='equipped')

	class Meta:
		model = models.InventoryRecord
		fields = ('url', 'owner', 'item', 'quantity', 'equipped', )

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
		fields = ('url', 'name', 'slug', 'mobs', )

class AbilitySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Ability
		fields = ('url', 'name', 'description', 'power', 'requires', 'element', 'description')
		lookup_field = 'slug'
		read_only_fields = ('name', 'description', 'power', 'requires', 'element', 'description')

class LearntAbilitySerializer(serializers.HyperlinkedModelSerializer):
	character = serializers.HyperlinkedRelatedField(
			view_name='character-detail',
			lookup_field='name',
			read_only=True,
		)

	ability = serializers.HyperlinkedRelatedField(
			view_name='ability-detail',
			lookup_field='slug',
		)
	class Meta:
		model = models.LearntAbility
		fields = ('id', 'character', 'ability')

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

	img = serializers.Field(source='img')

	class Meta:
		model = models.Mob
		fields = ('url', 'name', 'drops',
					'stre', 'atk', 'mag', 'spd', 'defense', 'mdefense', 'vit', 'img', )
