from rest_framework import viewsets
from rest_framework.decorators import link, renderer_classes, api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from permissions import IsOwnerOrReadOnly
#from models import Word
from models import User
from serializers import UserSerializer

from announce import AnnounceClient
announce_client = AnnounceClient()

@api_view(['GET'])
@renderer_classes((TemplateHTMLRenderer,))
def root(request, format=None):
	return Response(template_name='base.html')

@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		})

#remember:
# Custom actions which use the @link decorator will respond to GET requests.
# We could have instead used the @action decorator if we wanted an action that responded to POST requests.
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	#permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

	# def pre_save(self, obj):
	# 	obj.owner = self.request.user
	# 	announce_client.broadcast(
	# 		#obj.owner.pk,
	# 		'notifications',
	# 		data={'msg': 'You posted LOL'}
	# 		)
	# 	print 'SAVED AND EMITTED!!'

	# def post_save(self, obj, created=False):
	# 	if created:
	# 		print 'OBJECT CREATED'
	# 		announce_client.broadcast('notifications', data={'msg': obj.word})
	# 		status = announce_client.get_room_status('notifications')
	# 		print 'NOTIFICATIONS CHANNEL STATUS'
	# 		print status