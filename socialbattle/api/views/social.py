from rest_framework.generics import get_object_or_404
from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.decorators import action, link
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers
from socialbattle.api.permissions import IsFromUser, IsAuthor

### USER
# GET, POST: /users/
# GET, DELETE, PUT: /users/{username}/
class UserViewSet(viewsets.GenericViewSet,
					mixins.ListModelMixin,
					mixins.RetrieveModelMixin,
					mixins.UpdateModelMixin):
	queryset = models.User.objects.all()
	serializer_class = serializers.UserSerializer
	lookup_field = 'username'
	#permission_classes = [permissions.IsAdminUser, ]

### FELLOWSHIP
# GET: /users/{username}/follow[(ing)|(ers)]/
# POST: /users/{username}/following/
# GET, DELETE: /fellowship/{pk}/
class UserFollowingViewSet(viewsets.GenericViewSet, 
						mixins.CreateModelMixin,
						mixins.ListModelMixin):
	serializer_class = serializers.FellowshipSerializer

	def get_queryset(self):
		queryset = models.Fellowship.objects.all()
		username = self.kwargs.get('username')
		if username:
			queryset = queryset.filter(from_user__username=username).all()
		return queryset

	def pre_save(self, obj):
		obj.from_user = self.request.user

class UserFollowersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	serializer_class = serializers.FellowshipSerializer

	def get_queryset(self):
		queryset = models.Fellowship.objects.all()
		username = self.kwargs.get('username')
		if username:
			queryset = queryset.filter(to_user__username=username).all()
		return queryset

	def pre_save(self, obj):
		obj.from_user = self.request.user

class FellowshipViewSet(viewsets.GenericViewSet,
						mixins.DestroyModelMixin,
						mixins.RetrieveModelMixin):
	queryset = models.Fellowship.objects.all()
	serializer_class = serializers.FellowshipSerializer
	permission_classes = [permissions.IsAuthenticated, IsFromUser, ]

### POST
# GET, POST: /rooms/relax/{room_slug}/posts/
# GET: /users/{username}/posts/
# GET, PUT, DELETE: /posts/{pk}/
class RoomPostViewSet(viewsets.GenericViewSet,
						mixins.CreateModelMixin,
						mixins.ListModelMixin):
	queryset = models.Post.objects
	serializer_class = serializers.PostSerializer

	def get_queryset(self):
		queryset = models.Post.objects.all()
		room_slug = self.kwargs.get('room_slug', None)
		if room_slug:
			queryset = queryset.filter(room__slug=room_slug).all()
		return queryset

	def pre_save(self, obj):
		room_slug = self.kwargs.get('room_slug')
		room = get_object_or_404(models.RelaxRoom.objects.all(), slug=room_slug)
		room = serializers.RelaxRoomSerializer(room, context=self.get_serializer_context())
		obj.room = room.object
		obj.author = self.request.user

class UserPostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	serializer_class = serializers.PostSerializer

	def get_queryset(self):
		queryset = models.Post.objects.all()
		username = self.kwargs.get('username', None)
		if username:
			queryset = queryset.filter(author__username=username).all()
		return queryset	

class PostViewset(viewsets.GenericViewSet,
					mixins.RetrieveModelMixin,
					mixins.DestroyModelMixin,
					mixins.UpdateModelMixin):
	queryset = models.Post.objects.all()
	serializer_class = serializers.PostSerializer
	permission_classes = [permissions.IsAuthenticated, IsAuthor, ]

### COMMENT
# GET, POST: /posts/{pk}/comments/
# GET, PUT, DELETE: /comments/{pk}/
class PostCommentViewSet(viewsets.GenericViewSet,
							mixins.ListModelMixin,
							mixins.CreateModelMixin):
	serializer_class = serializers.CommentSerializer

	def get_queryset(self):
		queryset = models.Comment.objects.all()
		post_pk = self.kwargs.get('pk')
		if post_pk:
			queryset = queryset.filter(post__pk=post_pk).all()
		return queryset

	def pre_save(self, obj):
		post_pk = self.kwargs.get('pk')
		post = get_object_or_404(models.Post.objects.all(), pk=post_pk)
		post = serializers.PostSerializer(post, context=self.get_serializer_context())
		obj.post = post.object
		obj.author = self.request.user


class CommentViewSet(viewsets.GenericViewSet,
					mixins.RetrieveModelMixin,
					mixins.DestroyModelMixin,
					mixins.UpdateModelMixin):
	queryset = models.Comment.objects.all()
	serializer_class = serializers.CommentSerializer
	permission_classes = [permissions.IsAuthenticated, IsAuthor, ]