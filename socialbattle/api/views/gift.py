from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status
from socialbattle.api.fake_serializers import AcceptSerializer
from socialbattle.api.models import Item
from socialbattle.api.serializers import ItemSerializer
from socialbattle.api.models import ExchangeRecord

from rest_framework.throttling import UserRateThrottle

class GiftRateThrottle(UserRateThrottle):
	scope = 'gifts'
	rate = '4/day'

class GiftViewSet(GenericViewSet, CreateModelMixin):
	model = Item
	serializer_class = AcceptSerializer
	throttle_classes = (GiftRateThrottle, )
	
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.DATA)

		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		character = serializer.object.character

		if character not in request.user.character_set.all():
			self.permission_denied(request)

		#getting random item
		item = Item.objects.order_by('?')[0]

		character.add_to_inventory(ExchangeRecord(item=item, quantity=1))

		data = ItemSerializer(item, context=self.get_serializer_context()).data
		
		return Response(data=data, status=status.HTTP_201_CREATED)