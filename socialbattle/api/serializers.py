from rest_framework import serializers
from socialbattle.api import models

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
		fields = ('url', 'username', 'password', 'email', 'img',
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

class FollowingSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='fellowship-detail',
			lookup_field='pk',
		)

	to_user = UserSerializer(read_only=True)

	class Meta:
		model = models.Fellowship
		fields = ('url', 'to_user')

class FollowersSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='fellowship-detail',
			lookup_field='pk',
		)

	from_user = UserSerializer(read_only=True)

	class Meta:
		model = models.Fellowship
		fields = ('url', 'from_user')

class RelaxRoomSerializer(DynamicHyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='relaxroom-detail',
			lookup_field='slug',
		)

	class Meta:
		model = models.RelaxRoom
		fields = ('url', 'name', 'slug', 'fb_id',)

class ItemSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Item
		fields = ('url', 'name', 'cost', 'item_type', 'power', 'description', 'fb_id',)
		lookup_field = 'slug'

class ExchangeRecordCreateSerializer(serializers.HyperlinkedModelSerializer):
	item = serializers.HyperlinkedRelatedField(
		view_name='item-detail',
		lookup_field='slug',
	)

	class Meta:
		model = models.ExchangeRecord
		fields = ('item', 'quantity', 'given')

class ExchangeRecordGetSerializer(serializers.HyperlinkedModelSerializer):
	item = ItemSerializer(read_only=True)

	class Meta:
		model = models.ExchangeRecord
		fields = ('item', 'quantity', 'given')


class PostGetSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='post-detail',
			lookup_field='pk',
		)

	author = UserSerializer(fields=['url', 'username', 'img'], read_only=True)

	no_comments = serializers.Field(source='no_comments')

	character = serializers.HyperlinkedRelatedField(
		view_name='character-detail',
		lookup_field='name',
	)

	room = RelaxRoomSerializer(fields=['url', 'name', 'slug'], read_only=True)

	exchanged_items = ExchangeRecordGetSerializer(many=True, read_only=True)

	give_guils = serializers.IntegerField(required=False)
	receive_guils = serializers.IntegerField(required=False)

	class Meta:
		model = models.Post
		fields = ('url', 'content', 'author', 'character', 'room', 'time',
					'exchanged_items', 'give_guils', 'receive_guils', 'opened', 'no_comments')
		read_only_fields = ('time', 'opened')

class PostCreateSerializer(PostGetSerializer):
	exchanged_items = ExchangeRecordCreateSerializer(many=True, read_only=True)

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

	img = serializers.Field(source='img')
	defense = serializers.Field(source='defense')
	mdefense = serializers.Field(source='mdefense')
	atk = serializers.Field(source='atk')

	class Meta:
		model = models.Character
		fields = (
			'url', 'name', 'level', 'guils', 'owner',
			'ap', 'max_hp', 'max_mp', 'curr_hp', 'curr_mp',
			'stre', 'vit', 'mag', 'spd', 'defense', 'mdefense', 'atk',
			'img', 'fb_id',
		)

		read_only_fields = ('level', 'ap', 'guils', 'max_hp', 'max_mp', 'stre', 'vit', 'mag', 'spd',
							'curr_hp', 'curr_mp', 'fb_id')

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

	item = ItemSerializer(read_only=True)

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

	class Meta:
		model = models.PVERoom
		fields = ('url', 'name', 'slug', 'fb_id',)

class AbilitySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Ability
		fields = ('url', 'name', 'description', 'power', 'requires', 'element',
			'description', 'ap_required', 'mp_required', )
		lookup_field = 'slug'
		read_only_fields = ('name', 'description', 'power', 'requires', 'element',
			'description', 'ap_required', 'mp_required')

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
		fields = ('character', 'ability')

class MobSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='mob-detail',
			lookup_field='slug',
		)

	img = serializers.Field(source='img')

	class Meta:
		model = models.Mob
		fields = ('url', 'name', 'slug', 'hp',
					'stre', 'atk', 'mag', 'spd', 'defense', 'mdefense', 'vit', 'img', 'level', 'fb_id', )

class JSONField(serializers.WritableField):
	def to_native(self, obj):
		return obj

class ActivitySerializer(serializers.ModelSerializer):
	data = JSONField()
	class Meta:
		model = models.Activity
		fields = ('event', 'data', )

class NotificationSerializer(serializers.HyperlinkedModelSerializer):
	user = UserSerializer(fields=['url', 'username', 'img'], read_only=True)
	activity = ActivitySerializer(read_only=True)

	class Meta:
		model = models.Notification
		fields = ('url', 'id', 'user', 'activity', 'read')