from rest_framework import serializers
from socialbattle.private import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
	no_following = serializers.Field(source='no_following')	
	no_followers = serializers.Field(source='no_followers')

	class Meta:
		model = models.User
		fields = ('url', 'id', 'username', 'first_name', 'last_name', 'password','email', 'img',
					'no_following', 'no_followers', )
		write_only_fields = ('password', )
		read_only_fields = ('img', )
		lookup_field = 'username'

class FellowshipCreateSerializer(serializers.HyperlinkedModelSerializer):
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

class FellowshipGetSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(
			view_name='fellowship-detail',
			lookup_field='pk',
		)

	from_user = serializers.HyperlinkedRelatedField(
			view_name='user-detail',
			lookup_field='username',
			read_only=True,
		)

	to_user = UserSerializer()

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

	author_username = serializers.Field(source='author.username')
	room_name = serializers.Field(source='room.name')

	class Meta:
		model = models.Post
		fields = ('url', 'id', 'content', 'author', 'author_username', 'room', 'room_name', 'time' )

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

	author_username = serializers.Field(source='author.username')

	class Meta:
		model = models.Comment
		fields = ('url', 'content', 'author', 'post', 'time', 'author_username')

class ItemSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Item
		fields = ('url', 'name', 'cost', 'item_type', 'power')
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

		read_only_fields = ('name', 'level', 'ap', 'guils', 'max_hp', 'max_mp', 'stre', 'vit', 'mag', 'spd',
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

class AbilitySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Ability
		fields = ('url', 'name', 'description', 'power', 'requires', 'element')
		lookup_field = 'slug'
		read_only_fields = ('name', 'description', 'power', 'requires', 'element')

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
