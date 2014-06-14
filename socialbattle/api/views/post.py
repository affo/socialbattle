from rest_framework.generics import get_object_or_404
from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers
from socialbattle.api.permissions import IsAuthor

class PostMixin(object):
	def create_update_post(self, post, request):

		#cannot offer some other character's items!
		if post.character not in request.user.character_set.all():
			self.permission_denied(request)

		exchanged_items_field = request.DATA.get('exchanged_items', None)
		if exchanged_items_field:
			item_serializer = serializers.ExchangeRecordSerializer(
				data=exchanged_items_field,
				context=self.get_serializer_context(),
				many=True
			)

			if not item_serializer.is_valid():
				return Response(data=item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

			items = item_serializer.object

			#check exchange parameters are admissible
			for item in items:
				if not post.character.check_exchange(item):
					data = {
						'msg': 'Cannot offer %d of item %s' % (item.quantity, item.item.name)
					}
					return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

		self.pre_save(post)
		self.object = post_serializer.save(force_insert=True)

		if items:
			for item in items:
				item.post = post
				item.save()

		data = self.get_serializer(post).data

		headers = self.get_success_headers(data)
		return Response(data=data, status=status.HTTP_201_CREATED, headers=headers)


### POST
# GET, POST: /rooms/relax/{room_slug}/posts/
# GET: /users/{username}/posts/
# GET, PUT, DELETE: /posts/{pk}/
class RoomPostViewSet(viewsets.GenericViewSet,
						mixins.CreateModelMixin,
						mixins.ListModelMixin):
	queryset = models.Post.objects.all()
	serializer_class = serializers.PostSerializer
	paginate_by = 5
	paginate_by_param = 'limit'
	max_paginate_by = 30

	def get_queryset(self):
		queryset = models.Post.objects.all()
		room_slug = self.kwargs.get('room_slug', None)
		if room_slug:
			queryset = queryset.filter(room__slug=room_slug).order_by('-time').all()
		return queryset

	def pre_save(self, obj):
		room_slug = self.kwargs.get('room_slug')
		room = get_object_or_404(models.RelaxRoom.objects.all(), slug=room_slug)
		room = serializers.RelaxRoomSerializer(room, context=self.get_serializer_context())
		obj.room = room.object
		obj.author = self.request.user

	#custom create to create exchange records
	def create(self, request, *args, **kwargs):
		items = None
		post_serializer = self.get_serializer(data=request.DATA)

		if not post_serializer.is_valid():
			return Response(data=post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		post = post_serializer.object

		#cannot offer some other character's items!
		if post.character not in request.user.character_set.all():
			self.permission_denied(request)

		exchanged_items_field = request.DATA.get('exchanged_items', None)
		if exchanged_items_field:
			item_serializer = serializers.ExchangeRecordSerializer(
				data=exchanged_items_field,
				context=self.get_serializer_context(),
				many=True
			)

			if not item_serializer.is_valid():
				return Response(data=item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

			items = item_serializer.object

			#check exchange parameters are admissible
			for item in items:
				if not post.character.check_exchange(item):
					data = {
						'msg': 'Cannot offer %d of item %s' % (item.quantity, item.item.name)
					}
					return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

		self.pre_save(post)
		self.object = post_serializer.save(force_insert=True)

		if items:
			for item in items:
				item.post = post
				item.save()

		data = self.get_serializer(post).data

		headers = self.get_success_headers(data)
		return Response(data=data, status=status.HTTP_201_CREATED, headers=headers)

class UserPostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	serializer_class = serializers.PostSerializer
	paginate_by = 5
	paginate_by_param = 'limit'
	max_paginate_by = 30

	def get_queryset(self):
		queryset = models.Post.objects.all()
		username = self.kwargs.get('username', None)
		if username:
			queryset = queryset.filter(author__username=username).order_by('-time').all()
		return queryset	

class PostViewset(viewsets.GenericViewSet,
					mixins.RetrieveModelMixin,
					mixins.DestroyModelMixin,
					mixins.UpdateModelMixin):
	queryset = models.Post.objects.all()
	serializer_class = serializers.PostSerializer
	permission_classes = [permissions.IsAuthenticated, IsAuthor]

	def update(self, request, *args, **kwargs):
		partial = kwargs.pop('partial', False)
		self.object = self.get_object_or_none()

		post_serializer = self.get_serializer(self.object, data=request.DATA, files=request.FILES, partial=partial)
		items = None

		if not post_serializer.is_valid():
			return Response(data=post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		post = post_serializer.object

		#cannot offer some other character's items!
		if post.character not in request.user.character_set.all():
			self.permission_denied(request)

		exchanged_items_field = request.DATA.get('exchanged_items', None)
		if exchanged_items_field:
			item_serializer = serializers.ExchangeRecordSerializer(
				data=exchanged_items_field,
				context=self.get_serializer_context(),
				many=True
			)

			if not item_serializer.is_valid():
				return Response(data=item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

			#delete all previous exchanges
			previous_exchanges = list(models.ExchangeRecord.objects.filter(post=post).all())
			for p in previous_exchanges:
				p.delete()

			items = item_serializer.object

			#check exchange parameters are admissible
			for item in items:
				if not post.character.check_exchange(item):
					data = {
						'msg': 'Cannot offer %d of item %s' % (item.quantity, item.item.name)
					}
					return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

		self.object = post_serializer.save(force_update=True)

		if items:
			for item in items:
				item.post = post
				item.save()

		data = self.get_serializer(post).data
		return Response(data, status=status.HTTP_200_OK)

### COMMENT
# GET, POST: /posts/{pk}/comments/
# GET, PUT, DELETE: /comments/{pk}/
class PostCommentViewSet(viewsets.GenericViewSet,
							mixins.ListModelMixin,
							mixins.CreateModelMixin):
	serializer_class = serializers.CommentSerializer
	paginate_by = 5
	paginate_by_param = 'limit'
	max_paginate_by = 30

	def get_queryset(self):
		queryset = models.Comment.objects.all()
		post_pk = self.kwargs.get('pk')
		if post_pk:
			queryset = queryset.filter(post__pk=post_pk).order_by('-time').all()
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