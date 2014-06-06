from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from socialbattle.api import models
from socialbattle.api import serializers

### MOB
# GET: /room/pve/{room_slug}/mobs/
# GET: /mobs/{mob_name}
class RoomMobViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of the available mobs for the chosen PVE room
	'''
	serializer_class = serializers.MobSerializer

	def get_queryset(self):
		queryset = models.Mob.objects.all()
		room_slug = self.kwargs.get('room_slug')
		if room_slug:
			queryset = queryset.filter(pveroom__slug=room_slug).all()
		return queryset

from socialbattle.api.views.action import use_ability
from django.db import models as dj_models
from rest_framework import serializers as drf_serializers
class MobAbilityUsage(dj_models.Model):
	attacked = dj_models.ForeignKey(models.Character, null=True)
	ability = dj_models.ForeignKey(models.Ability)

class MobAbilityUsageSerializer(drf_serializers.HyperlinkedModelSerializer):
	ability = drf_serializers.HyperlinkedRelatedField(
		view_name='ability-detail',
		lookup_field='slug'
	)

	attacked = drf_serializers.HyperlinkedRelatedField(
		view_name='character-detail',
		lookup_field='name',
		required=False,
	)

	class Meta:
		model = MobAbilityUsage
		fields = ('attacked', 'ability', )

class MobViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	queryset = models.Mob.objects.all()
	serializer_class = serializers.MobSerializer
	lookup_field = 'slug'

	@action(methods=['POST'], serializer_class=MobAbilityUsageSerializer)
	def use_ability(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.DATA)

		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		attacker = self.get_object()
		ability = serializer.object.ability
		attacked = serializer.object.attacked
		if not attacked:
			attacked = attacker

		return use_ability(attacker, attacked, ability)

	@action(methods=['GET'], serializer_class=serializers.AbilitySerializer)
	def abilities(self, request, *args, **kwargs):
		mob = self.get_object()
		abilities = mob.abilities.all()
		return Response(self.get_serializer(abilities, many=True).data, status=status.HTTP_200_OK)