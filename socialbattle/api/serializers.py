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

	abilities = serializers.HyperlinkedRelatedField(
			view_name='ability-detail',
			lookup_field='slug',
			many=True,
		)

	class Meta:
		model = models.Character
		fields = (
			'url', 'name', 'level', 'guils', 'owner',
			'ap', 'hp', 'mp',
			'power', 'mpower',
			'abilities',
		)

		read_only_fields = ('name', 'level', 'ap', 'guils', 'hp', 'mp', 'power', 'mpower', )

class InventoryRecordCreateSerializer(serializers.HyperlinkedModelSerializer):
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
	equipped = serializers.Field(source='equipped')

	class Meta:
		model = models.InventoryRecord
		fields = ('url', 'owner', 'item', 'quantity', 'equipped', )

class InventoryRecordUpdateSerializer(serializers.HyperlinkedModelSerializer):
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

	class Meta:
		model = models.Mob
		fields = ('url', 'name', 'drops', )

class BattleSerializer(serializers.HyperlinkedModelSerializer):
	fields = serializers.HyperlinkedIdentityField(
		view_name='battle-detail',
		lookup_field='pk',
	)
	
	class Meta:
		model = models.Battle
		fields = ('url', 'character', 'mob', )
		read_only_fields = ('url', 'character', 'mob', )
		lookup_field = 'slug'