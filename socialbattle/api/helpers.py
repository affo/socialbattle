from django.db import models
from rest_framework import serializers
from socialbattle.api.models import Character, Item

class Transaction(models.Model):
	OPERATION_TYPE = (('B', 'Buy'), ('S', 'Sell'), )
	character = models.ForeignKey(Character)

	item = models.ForeignKey(Item)
	quantity = models.IntegerField(default=0)
	operation = models.CharField(max_length=1, choices=OPERATION_TYPE)

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
	character = serializers.HyperlinkedRelatedField(
		view_name='character-detail',
		lookup_field='name',
		read_only=True,
	)

	class Meta:
		model = Transaction
		fields = ('character', 'item', 'quantity', 'operation', )
