from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers

### ROOM
# GET: /rooms/
# GET: /rooms/pve/
# GET: /rooms/pve/{room_slug}
# GET: /rooms/relax/
# GET: /rooms/relax/{room_slug}
class RelaxRoomViewSet(viewsets.GenericViewSet,
						mixins.ListModelMixin,
						mixins.RetrieveModelMixin):
	queryset = models.RelaxRoom.objects.all()
	serializer_class = serializers.RelaxRoomSerializer
	lookup_field = 'slug'

class PVERoomViewSet(viewsets.GenericViewSet,
						mixins.ListModelMixin,
						mixins.RetrieveModelMixin):
	queryset = models.PVERoom.objects.all()
	serializer_class = serializers.PVERoomSerializer
	lookup_field = 'slug'

class RoomViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of all rooms (pve and relax)
	'''

	def list(self, request, *args, **kwargs):
		try:
			query = request.QUERY_PARAMS['query']
			relax = models.RelaxRoom.objects.filter(name__icontains=query)
			pve = models.PVERoom.objects.filter(name__icontains=query)
		except:
			relax = models.RelaxRoom.objects.all()
			pve = models.PVERoom.objects.all()

		relax = serializers.RelaxRoomSerializer(relax, context=self.get_serializer_context(), many=True).data
		pve = serializers.PVERoomSerializer(pve, context=self.get_serializer_context(), many=True).data

		return Response(relax + pve, status=status.HTTP_200_OK)