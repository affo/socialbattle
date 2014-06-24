from rest_framework.generics import get_object_or_404
from rest_framework import permissions, viewsets, mixins
from rest_framework.serializers import HyperlinkedRelatedField, HyperlinkedModelSerializer
from rest_framework.response import Response
from rest_framework import status
from socialbattle.api.models import Character, InventoryRecord, Item
from socialbattle.api import serializers
from socialbattle.api.permissions import IsOwner
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from socialbattle.api.utils import NotifyMixin

class Transaction(models.Model):
	OPERATION_TYPE = (('B', 'Buy'), ('S', 'Sell'), )
	character = models.ForeignKey(Character)

	item = models.ForeignKey(Item)
	quantity = models.IntegerField(default=0)
	operation = models.CharField(max_length=1, choices=OPERATION_TYPE)

class TransactionSerializer(HyperlinkedModelSerializer):
	character = HyperlinkedRelatedField(
		view_name='character-detail',
		lookup_field='name',
		read_only=True,
	)

	class Meta:
		model = Transaction
		fields = ('character', 'item', 'quantity', 'operation', )

### TRANSACTION
# POST: /characters/{character_name}/transactions/
class TransactionViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, NotifyMixin):
	'''
		From this view it is possible for a character to buy and sell items.
	'''
	serializer_class = TransactionSerializer

	def create(self, request, *args, **kwargs):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(Character.objects.all(), name=name)
		if character.owner != request.user:
			self.permission_denied(request)

		BUY_OP = Transaction.OPERATION_TYPE[0][0]
		SELL_OP = Transaction.OPERATION_TYPE[1][0]

		serializer = self.get_serializer(data=request.DATA, files=request.FILES)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		transaction = serializer.object	

		if transaction.operation == BUY_OP:	
			if transaction.item.cost * transaction.quantity > character.guils and transaction.operation:
				return Response(
							data={'msg': 'Not enough money to buy this item'},
							status=status.HTTP_400_BAD_REQUEST
						)

			try:
				record = InventoryRecord.objects.get(owner=character, item=transaction.item)
				record.quantity += transaction.quantity
				record.save()
			except ObjectDoesNotExist:
				record = InventoryRecord.objects.create(
							owner=character,
							item=transaction.item, 
							quantity=transaction.quantity
						)

			character.guils -= (transaction.item.cost * transaction.quantity)

		elif transaction.operation == SELL_OP:
			try:
				record = InventoryRecord.objects.get(owner=character, item=transaction.item)
				if transaction.quantity > record.quantity:
					return Response(
							data={'msg': 'You do not have as much items of that type'},
							status=status.HTTP_400_BAD_REQUEST
						)

				record.quantity -= transaction.quantity
				if record.quantity == 0:
					record.delete()
				else:
					record.save()
			except ObjectDoesNotExist:
				return Response(
						data={'msg': 'The specified character does not own the specified item'},
						status=status.HTTP_400_BAD_REQUEST
					)

			character.guils += (transaction.item.cost / 2) * transaction.quantity

		character.save()
		record = serializers.InventoryRecordSerializer(record, context=self.get_serializer_context()).data
		data = {
			'inventory_record': record,
			'guils_left': character.guils,
		}

		#notify
		self.notify_followers(user=request.user, event='activity-transaction', data={
				'username': request.user.username,
				'character_name': character.name,
				'op': transaction.operation,
				'item_name': transaction.item.name,
			})

		return Response(data=data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(data))