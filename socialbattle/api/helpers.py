from django.db import models
from rest_framework import serializers
from socialbattle.api.models import Character, Item, Ability, Target

class Transaction(models.Model):
	OPERATION_TYPE = (('B', 'Buy'), ('S', 'Sell'), )
	character = models.ForeignKey(Character)

	item = models.ForeignKey(Item)
	quantity = models.IntegerField(default=0)
	operation = models.CharField(max_length=1, choices=OPERATION_TYPE)

class Attack(models.Model):
	ability = models.ForeignKey(Ability)
	target = models.ForeignKey(Target)

class Usage(models.Model):
	item = models.ForeignKey(Item)
	target = models.ForeignKey(Target)

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
	character = serializers.HyperlinkedRelatedField(
		view_name='character-detail',
		lookup_field='name',
		read_only=True,
	)

	class Meta:
		model = Transaction
		fields = ('character', 'item', 'quantity', 'operation', )

class AbilityUsageSerializer(serializers.HyperlinkedModelSerializer):
	ability = serializers.HyperlinkedRelatedField(
		view_name='ability-detail',
		lookup_field='slug'
	)

	target = serializers.HyperlinkedRelatedField(
		view_name='target-detail',
		lookup_field='pk'
	)

	class Meta:
		model = Attack
		fields = ('ability', 'target')

class ItemUsageSerializer(serializers.HyperlinkedModelSerializer):
	item = serializers.HyperlinkedRelatedField(
		view_name='item-detail',
		lookup_field='slug'
	)

	target = serializers.HyperlinkedRelatedField(
		view_name='target-detail',
		lookup_field='pk'
	)

	class Meta:
		model = Usage
		fields = ('item', 'target')