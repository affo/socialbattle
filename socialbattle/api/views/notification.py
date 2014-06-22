from rest_framework.generics import get_object_or_404
from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from socialbattle.api import models
from socialbattle.api import serializers

class NotificationViewSet(viewsets.GenericViewSet,
							mixins.RetrieveModelMixin,
							mixins.UpdateModelMixin):
	queryset = models.Notification.objects.all()
	serializer_class = serializers.NotificationSerializer

class UserNotificationViewSet(viewsets.GenericViewSet,
							mixins.ListModelMixin):
	serializer_class = serializers.NotificationSerializer
	paginate_by = 7
	paginate_by_param = 'limit'
	max_paginate_by = 30

	def get_queryset(self):
		user = get_object_or_404(models.User.objects.all(), username=self.kwargs['username'])
		return models.Notification.objects.filter(user=user).all()

	@action(methods=['GET'])
	def unread(self, request, *args, **kwargs):
		user = get_object_or_404(models.User.objects.all(), username=self.kwargs['username'])
		n = models.Notification.objects.filter(user=user, read=False).all()

		return Response(data=self.get_serializer(n, many=True), status=status.HTTP_200_OK)

class UserUnreadNotificationViewSet(viewsets.GenericViewSet,
							mixins.ListModelMixin):
	serializer_class = serializers.NotificationSerializer
	paginate_by = 7
	paginate_by_param = 'limit'
	max_paginate_by = 30

	def get_queryset(self):
		user = get_object_or_404(models.User.objects.all(), username=self.kwargs['username'])
		return models.Notification.objects.filter(user=user, read=False).all()