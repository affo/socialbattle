from socialbattle.private import mechanics
from socialbattle.public import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

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
	serializer = serializers.AttackSerializer(data=request.DATA)
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
	serializer = serializers.CtSerializer(data=request.DATA)
	if serializer.is_valid():
		obj = serializer.object
		ct = mechanics.get_charge_time(obj, obj)
		return Response({'ct': ct}, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
	serializer = serializers.StatSerializer(data=request.DATA)
	if serializer.is_valid():
		obj = serializer.object
		stat = mechanics.get_stat(obj.lvl, obj.stat)
		return Response({obj.stat: stat}, status=status.HTTP_200_OK)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#################
from socialbattle.private.views import user
class UserViewSet(user.UserViewSet):
	serializer_class = serializers.UserSerializer
	allowed_methods = ('GET', )
	
	pass