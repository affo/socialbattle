from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from socialbattle.private import models
from socialbattle.private import serializers
from socialbattle.private.permissions import IsFromUser, IsAuthor

### USER
# GET, POST: /users/
# GET, PUT: /users/{username}/
class UserViewSet(viewsets.GenericViewSet,
					mixins.ListModelMixin,
					mixins.CreateModelMixin,
					mixins.UpdateModelMixin,
					mixins.RetrieveModelMixin):
	queryset = models.User.objects.all()
	serializer_class = serializers.UserSerializer
	lookup_field = 'username'

	def list(self, request, *args, **kwargs):
		try:
			query = request.QUERY_PARAMS['query']
		except:
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

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.DATA, files=request.FILES)
		if serializer.is_valid():
			user = serializer.object
			username = user.username
			email = user.email
			password = user.password
			user = models.User.objects.create_user(username, email, password)
			user = serializers.UserSerializer(user).data
			return Response(user, status=status.HTTP_201_CREATED,
							headers=self.get_success_headers(user))
		
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### FELLOWSHIP
# GET: /users/{username}/follow[(ing)|(ers)]/
# POST: /users/{username}/following/
# GET, DELETE: /fellowship/{pk}/
class UserFollowingViewSet(viewsets.GenericViewSet, 
						mixins.CreateModelMixin,
						mixins.ListModelMixin):
	serializer_class = serializers.UserSerializer

	def get_serializer_class(self):
		if self.request.method == 'POST':
			return serializers.FellowshipSerializer
		else:
			return self.serializer_class

	def get_queryset(self):
		queryset = models.User.objects.all()
		username = self.kwargs.get('username')
		if username:
			queryset = queryset.get(username=username).follows.all()
		return queryset

	def pre_save(self, obj):
		obj.from_user = self.request.user

class UserFollowersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	serializer_class = serializers.UserSerializer

	def get_queryset(self):
		queryset = models.User.objects.all()
		username = self.kwargs.get('username')
		if username:
			queryset = queryset.get(username=username).followss.all()
		return queryset

	def pre_save(self, obj):
		obj.from_user = self.request.user

class FellowshipViewSet(viewsets.GenericViewSet,
						mixins.DestroyModelMixin,
						mixins.RetrieveModelMixin):
	queryset = models.Fellowship.objects.all()
	serializer_class = serializers.FellowshipSerializer
	permission_classes = [permissions.IsAuthenticated, IsFromUser, ]