from rest_framework import serializers
from models import Word
from django.contrib.auth.models import User

class WordSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.Field(source='owner.username')
	#highlight = serializers.HyperlinkedIdentityField(view_name='word-highlight', format='html')

	class Meta:
		model = Word
		fields = ('id', 'url', 'word', 'owner')

class UserSerializer(serializers.HyperlinkedModelSerializer):
	words = serializers.HyperlinkedRelatedField(many=True, view_name='word-detail')

	class Meta:
		model = User
		fields = ('url', 'username', 'words')