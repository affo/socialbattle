from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers
from socialbattle.api.permissions import IsFromUser

class UserList(generics.ListAPIView):
	model = models.User
	serializer_class = serializers.UserSerializer
	#permission_classes = [permissions.IsAdminUser, ]


class UserDetail(generics.RetrieveUpdateAPIView):
	model = models.User
	serializer_class = serializers.UserSerializer
	lookup_field = 'username'


class FollowListViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
	queryset = models.Fellowship.objects.all()
	serializer_class = serializers.FellowshipSerializer
	permission_classes = [permissions.IsAuthenticated, IsFromUser, ]

	@action(methods=['GET', ], permission_classes=[permissions.IsAuthenticated, ])
	def followx(self, request, username, direction, format=None):
		if direction == 'ing':
			follows = self.get_queryset().filter(from_user__username=username).all()
			follows = serializers.FellowshipSerializer(follows, context=self.get_serializer_context(), many=True).data
			data = follows
		elif direction == 'ers':
			followed = self.get_queryset().filter(to_user__username=username).all()
			followed = serializers.FellowshipSerializer(followed, context=self.get_serializer_context(), many=True).data
			data = followed
		else:
			message = "A user is followING or has followERS, a user cannot be/have follow%s" % direction
			return Response(data={'message': message}, status=status.HTTP_400_BAD_REQUEST)
		return Response(data)

	@action(methods=['POST', ], permission_classes=[permissions.IsAuthenticated, IsFromUser, ])
	def auth_create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.DATA, files=request.FILES)
		if serializer.is_valid():
			obj = serializer.object
			self.check_object_permissions(request, obj)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		return self.create(request, *args, **kwargs)


class FollowDetailViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin):
	queryset = models.Fellowship.objects.all()
	serializer_class = serializers.FellowshipSerializer
	permission_classes = [permissions.IsAuthenticated, IsFromUser, ]

class UserPostListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	queryset = models.Post.objects
	serializer_class = serializers.PostSerializer

	def get_queryset(self):
		username = self.kwargs.get('username')

		if username:
			return self.queryset.filter(author__username=username).all()
		return None

class RelaxRoomPostListViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
	queryset = models.Post.objects
	serializer_class = serializers.PostSerializer

	def get_queryset(self):
		room_name = self.kwargs.get('name')

		if room_name:
			return self.queryset.filter(room__name=room_name).all()
		return None


class PostDetailViewSet(viewsets.GenericViewSet, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
	queryset = models.Post.objects.all()
	serializer_class = serializers.PostSerializer