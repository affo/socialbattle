from rest_framework import viewsets
from rest_framework.decorators import link, renderer_classes, api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from permissions import IsOwnerOrReadOnly
from models import Word
from django.contrib.auth.models import User
from serializers import WordSerializer, UserSerializer


@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
def root(request, format=None):
	return Response(template_name='base.html')

@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'words': reverse('word-list', request=request, format=format)
		})

class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
 	serializer_class = UserSerializer

#remember:
# Custom actions which use the @link decorator will respond to GET requests.
# We could have instead used the @action decorator if we wanted an action that responded to POST requests.
class WordViewSet(viewsets.ModelViewSet):
	queryset = Word.objects.all()
	serializer_class = WordSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

	def pre_save(self, obj):
		obj.owner = self.request.user