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
def damage(request, *args, **kwargs):
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

@api_view(['POST'])
def exp(request, *args, **kwargs):
	'''
	Calculates the experience required to reach the specified level.    
	Sample input:

		{
			"lvl": 42
		}
	'''
	try:
		level = request.DATA['lvl']
		return Response({'exp': mechanics.get_exp(level)}, status=status.HTTP_200_OK)
	except:
		return Response({'lvl': 'this field is required'}, status=status.HTTP_400_BAD_REQUEST)

class Ct(object):
	def __init__(self, spd, ctf):
		self.spd = spd
		self.ctf = ctf

class CtSerializer(serializers.Serializer):
	spd = serializers.IntegerField()
	ctf = serializers.IntegerField()

	def restore_object(self, attrs, instance=None):
		if instance is not None:
			instance.spd = attrs.get('spd', instance.spd)
			instance.ctf = attrs.get('ctf', instance.ct)
			return instance
		return Ct(**attrs)

@api_view(['POST'])
def ct(request, *args, **kwargs):
	'''
	Calculates the charge time required to perform an attack, given:  
	- the speed of the attacker  
	- the charge time factor of the ability (in case of magics)  
	- the charge time factor of the weapon (in case of physical attack)  
	Sample input:

		{
			"spd": 18,
			"ctf": 30
		}
	'''
	serializer = CtSerializer(data=request.DATA)
	if serializer.is_valid():
		obj = serializer.object
		ct = mechanics.get_charge_time(obj, obj)
		return Response({'ct': ct}, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Stat(object):
	def __init__(self, lvl, stat):
		self.lvl = lvl
		self.stat = stat

class StatSerializer(serializers.Serializer):
	lvl = serializers.IntegerField()
	stat = serializers.CharField()

	def restore_object(self, attrs, instance=None):
		if instance is not None:
			instance.lvl = attrs.get('lvl', instance.lvl)
			instance.stat = attrs.get('stat', instance.ct)
			return instance
		return Stat(**attrs)

@api_view(['POST'])
def stat(request, *args, **kwargs):
	'''
	Calculates the stat specified from the level given.  
	The stat could be: `HP`, `MP`, `STR`, `MAG`, `SPD` or `VIT`.  
	Sample input:

		{
			"lvl": 25,
			"stat": "HP"
		}
	'''
	serializer = StatSerializer(data=request.DATA)
	if serializer.is_valid():
		obj = serializer.object
		stat = mechanics.get_stat(obj.lvl, obj.stat)
		return Response({obj.stat: stat}, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)