from rest_framework.generics import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from socialbattle.api import models
from socialbattle.api import serializers
from socialbattle.api.permissions import IsFromUser, IsAuthor

### USER
# GET: /users/
# GET, PUT: /users/{username}/
class UserViewSet(viewsets.GenericViewSet,
					mixins.ListModelMixin,
					mixins.RetrieveModelMixin):
	queryset = models.User.objects.all()
	serializer_class = serializers.UserSerializer
	lookup_field = 'username'

	def list(self, request, *args, **kwargs):
		try:
			query = request.QUERY_PARAMS['query']
			if not query: raise KeyError
		except KeyError:
			return Response(data={'msg': 'Query param needed (?query=<query_string>)'},
							status=status.HTTP_400_BAD_REQUEST)

		from django.db.models import Q
		users = models.User.objects.filter(
				Q(username__icontains=query) |
				Q(first_name__icontains=query) |
				Q(last_name__icontains=query)
			)

		return Response(data=serializers.UserSerializer(users, context=self.get_serializer_context(), many=True).data,
						status=status.HTTP_200_OK)

	@action(methods=['POST'], serializer_class=serializers.FellowshipSerializer)
	def isfollowing(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.DATA)
		if not serializer.is_valid():
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		from_user = self.get_object()
		to_user = serializer.object.to_user
		try:
			f = models.Fellowship.objects.get(from_user=from_user, to_user=to_user)
			data = {
				'is_following': True,
				'url': self.get_serializer(f).data['url'],
			}
		except ObjectDoesNotExist:
			data = {'is_following': False}

		return Response(data, status=status.HTTP_200_OK)

### FELLOWSHIP
# GET: /users/{username}/follow[(ing)|(ers)]/
# POST: /users/{username}/following/
# GET, DELETE: /fellowship/{pk}/
class UserFollowingViewSet(viewsets.GenericViewSet, 
						mixins.CreateModelMixin,
						mixins.ListModelMixin):
	serializer_class = serializers.FollowingSerializer

	class AlreadyFollowingError(Exception):
			def __init__(self, msg):
				self.msg = msg

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return serializers.FellowshipSerializer
		else:
			return self.serializer_class

	def get_queryset(self):
		username = self.kwargs.get('username')
		user = get_object_or_404(models.User.objects.all(), username=username)
		queryset = models.Fellowship.objects.filter(from_user=user).all()
		return queryset

	def pre_save(self, obj):
		if obj.to_user in self.get_queryset():
			raise self.AlreadyFollowingError('The fellowship specified already exists')

		obj.from_user = self.request.user

	def create(self, request, *args, **kwargs):
		try:
			return super(UserFollowingViewSet, self).create(request, *args, **kwargs)
		except self.AlreadyFollowingError as e:
			return Response(data={'msg': e.msg}, status=status.HTTP_400_BAD_REQUEST)


	def list(self, request, username, *args, **kwargs):
		try:
			query = request.QUERY_PARAMS['query']
			user = get_object_or_404(models.User.objects.all(), username=username)

			from django.db.models import Q
			users = user.follows.filter(
					Q(username__icontains=query) |
					Q(first_name__icontains=query) |
					Q(last_name__icontains=query)
				)
			
			return Response(self.get_serializer(users, many=True).data, status=status.HTTP_200_OK)
		except KeyError:
			return super(UserFollowingViewSet, self).list(request, *args, **kwargs)


class UserFollowersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	serializer_class = serializers.FollowersSerializer

	def get_queryset(self):
		username = self.kwargs.get('username')
		user = get_object_or_404(models.User.objects.all(), username=username)
		queryset = models.Fellowship.objects.filter(to_user=user).all()
		return queryset

class FellowshipViewSet(viewsets.GenericViewSet,
						mixins.DestroyModelMixin,
						mixins.RetrieveModelMixin):
	queryset = models.Fellowship.objects.all()
	serializer_class = serializers.FellowshipSerializer
	permission_classes = [permissions.IsAuthenticated, IsFromUser, ]