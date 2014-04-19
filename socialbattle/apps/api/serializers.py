from rest_framework import serializers
import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.User
		fields = ('id', 'url', 'username', 'follows')