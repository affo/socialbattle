from socialbattle.private import mechanics
from django.db import models
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from socialbattle.private.models import Ability

class Target(models.Model):
	atk = models.IntegerField(default=0)
	stre = models.IntegerField(default=0)
	mag = models.IntegerField(default=0)
	defense = models.IntegerField(default=0)
	mdefense = models.IntegerField(default=0)
	level = models.IntegerField(default=0)

class Ability(models.Model):
	power = models.IntegerField(default=0)
	element = models.CharField(
			max_length=1,
			choices=Ability.ELEMENTS,
			default=Ability.ELEMENTS[0][0],
	)

class Attack(models.Model):
	attacker = models.ForeignKey(Target)
	attacked = models.ForeignKey(Target)
	ability = models.ForeignKey(Ability)

class TargetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Target
		fields = ('atk', 'stre', 'mag', 'defense', 'mdefense', 'level')
	

class AbilitySerializer(serializers.ModelSerializer):
	element = serializers.CharField(required=False)
	class Meta:
		model = Ability
		fields = ('power', 'element')

class AttackSerializer(serializers.ModelSerializer):
	attacker = TargetSerializer()
	attacked = TargetSerializer()
	ability = AbilitySerializer()

	class Meta:
		model = Attack
		fields = ('attacker', 'attacked', 'ability')


@api_view(['POST'])
def get_damage(request, *args, **kwargs):
	'''
	Calculates the damage giving an attacker, the target and the ability used.  
	Sample input:

		{
			"attacker": {
				"level": 2,
				"stre": 8,
				"mag": 5,
				"defense": 4,
				"mdefense": 7,
				"atk": 8
			},

			"attacked": {
				"level": 2,
				"stre": 8,
				"mag": 5,
				"defense": 4,
				"mdefense": 7,
				"atk": 8
			},

			"ability": {
				"power": 5,
				"element": "N"
			}
		}
	'''
	serializer = AttackSerializer(data=request.DATA)
	if serializer.is_valid():
		attacker = serializer.object.attacker
		attacked = serializer.object.attacked
		ability = serializer.object.ability
		dmg = mechanics.calculate_damage(attacker, attacked, ability)
		return Response({'dmg': dmg}, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)