from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers
from socialbattle.api.permissions import IsFromUser, IsAuthor
from socialbattle.api.mixins import CreateWithPermissionModelMixin

class UserList(generics.ListAPIView):
	model = models.User
	serializer_class = serializers.UserSerializer
	#permission_classes = [permissions.IsAdminUser, ]


class UserDetail(generics.RetrieveUpdateAPIView):
	model = models.User
	serializer_class = serializers.UserSerializer
	lookup_field = 'username'

####################
#### FOLLOWING #####
####################
class FollowList(viewsets.GenericViewSet, mixins.CreateModelMixin):
	queryset = models.Fellowship.objects.all()
	serializer_class = serializers.FellowshipSerializer

	@action(methods=['GET', ])
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

	def pre_save(self, obj):
		obj.from_user = self.request.user


class FollowDetail(viewsets.GenericViewSet, mixins.DestroyModelMixin):
	queryset = models.Fellowship.objects.all()
	serializer_class = serializers.FellowshipSerializer
	permission_classes = [permissions.IsAuthenticated, IsFromUser, ]


####################
###### POSTS #######
####################
class UserPostList(viewsets.GenericViewSet, mixins.ListModelMixin):
	queryset = models.Post.objects
	serializer_class = serializers.PostSerializer

	def get_queryset(self):
		username = self.kwargs.get('username')

		if username:
			return self.queryset.filter(author__username=username).all()
		return None

class RelaxRoomPostList(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
	queryset = models.Post.objects
	serializer_class = serializers.PostSerializer

	def get_queryset(self):
		room_name = self.kwargs.get('name')

		if room_name:
			return self.queryset.filter(room__name=room_name).all()
		return None

	def pre_save(self, obj):
		room_name = self.kwargs.get('name')
		if not room_name:
			raise ValueError('Need a room name to create post')
		room = models.RelaxRoom.objects.get(name=room_name)
		room = serializers.RelaxRoomSerializer(room, context=self.get_serializer_context())
		obj.room = room.object
		obj.author = self.request.user

class PostDetail(
		viewsets.GenericViewSet,
		mixins.DestroyModelMixin,
		mixins.RetrieveModelMixin,
		mixins.UpdateModelMixin):
	queryset = models.Post.objects.all()
	serializer_class = serializers.PostSerializer
	permission_classes = [permissions.IsAuthenticated, IsAuthor, ]

####################
##### COMMENTS #####
####################
class PostCommentList(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
	queryset = models.Comment.objects
	serializer_class = serializers.CommentSerializer

	def get_queryset(self):
		post_pk = self.kwargs.get('pk')
		if post_pk:
			return self.queryset.filter(post__pk=post_pk).all()
		return None

	def pre_save(self, obj):
		post_pk = self.kwargs.get('pk')
		if not post_pk:
			raise ValueError('Need a post key to create a comment')
		post = models.Post.objects.get(pk=post_pk)
		post = serializers.PostSerializer(post, context=self.get_serializer_context())
		obj.post = post.object
		obj.author = self.request.user

class CommentDetail(
		viewsets.GenericViewSet,
		mixins.DestroyModelMixin,
		mixins.RetrieveModelMixin,
		mixins.UpdateModelMixin):
	queryset = models.Comment.objects.all()
	serializer_class = serializers.CommentSerializer
	permission_classes = [permissions.IsAuthenticated, IsAuthor, ]