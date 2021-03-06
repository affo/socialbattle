from socialbattle.api import models
from socialbattle.api import fake_models
from rest_framework import serializers

class TargetSerializer(serializers.ModelSerializer):
	class Meta:
		model = fake_models.Target
		fields = ('atk', 'stre', 'mag', 'defense', 'mdefense', 'level')
	

class AbilitySerializer(serializers.ModelSerializer):
	element = serializers.CharField(required=False)
	
	class Meta:
		model = fake_models.Ability
		fields = ('power', 'element')

class AttackSerializer(serializers.ModelSerializer):
	attacker = TargetSerializer()
	attacked = TargetSerializer()
	ability = AbilitySerializer()

	class Meta:
		model = fake_models.Attack
		fields = ('attacker', 'attacked', 'ability')

class CtSerializer(serializers.Serializer):
	spd = serializers.IntegerField()
	ctf = serializers.IntegerField()

	def restore_object(self, attrs, instance=None):
		if instance is not None:
			instance.spd = attrs.get('spd', instance.spd)
			instance.ctf = attrs.get('ctf', instance.ct)
			return instance
		return fake_models.Ct(**attrs)

class StatSerializer(serializers.Serializer):
	lvl = serializers.IntegerField()
	stat = serializers.CharField()

	def restore_object(self, attrs, instance=None):
		if instance is not None:
			instance.lvl = attrs.get('lvl', instance.lvl)
			instance.stat = attrs.get('stat', instance.ct)
			return instance
		return fake_models.Stat(**attrs)


## Fake models and serializers to handle accpetance of an offer
from rest_framework.serializers import HyperlinkedModelSerializer, HyperlinkedRelatedField
class AcceptSerializer(HyperlinkedModelSerializer):
	character = HyperlinkedRelatedField(view_name='character-detail', lookup_field="name")
	class Meta:
		model = fake_models.Accept
		fields = ('character', )