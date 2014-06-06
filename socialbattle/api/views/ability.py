from rest_framework.generics import get_object_or_404
from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers

### ABILITY
# GET: /characters/{character_name}/abilities/	
# GET, POST: /characters/{character_name}/abilities/next/
# GET: /abilities/{ability_name}
class CharacterAbilityViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of the learned abilities for the chosen character
	'''
	serializer_class = serializers.AbilitySerializer

	def list(self, request, *args, **kwargs):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)
		abilities = character.abilities.all()
		abilities = self.get_serializer(abilities, many=True).data
		return Response(data=abilities, status=status.HTTP_200_OK)

class CharacterNextAbilityViewSet(viewsets.GenericViewSet,
									mixins.ListModelMixin,
									mixins.CreateModelMixin):
	'''
		List of the available abilities that a character can learn
	'''
	serializer_class = serializers.LearntAbilitySerializer

	def list(self, request, *args, **kwargs):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)

		next = character.get_next_abilities()
		next = serializers.AbilitySerializer(next, context=self.get_serializer_context(), many=True).data
		return Response(data=next, status=status.HTTP_200_OK)

	def create(self, request, *args, **kwargs):
		name = self.kwargs.get('character_name')
		character = get_object_or_404(models.Character.objects.all(), name=name)

		if character.owner != request.user:
			self.permission_denied(request)

		serializer = self.get_serializer(data=request.DATA, files=request.FILES)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		to_learn = serializer.object
		ability = to_learn.ability
		if ability not in character.get_next_abilities():
			return Response({'msg': 'The ability specified cannot be learnt'},
							status=status.HTTP_400_BAD_REQUEST)

		if ability.ap_required > character.ap:
			return Response({'msg': 'Too much APs'},
							status=status.HTTP_400_BAD_REQUEST)

		character.ap -= ability.ap_required
		character.save()
		to_learn.character = character
		self.object = serializer.save(force_insert=True)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AbilityViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	queryset = models.Ability.objects.all()
	serializer_class = serializers.AbilitySerializer
	lookup_field='slug'
