from rest_framework.generics import get_object_or_404
from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from socialbattle.api import models
from socialbattle.api import serializers
from socialbattle.api.permissions import IsLoggedUserNoSafeMethods

class NotificationViewSet(viewsets.GenericViewSet,
							mixins.RetrieveModelMixin,
							mixins.UpdateModelMixin):
	queryset = models.Notification.objects.all()
	serializer_class = serializers.NotificationSerializer
	permission_classes = [permissions.IsAuthenticated, IsLoggedUserNoSafeMethods]

class UserNotificationViewSet(viewsets.GenericViewSet,
							mixins.ListModelMixin):
	serializer_class = serializers.NotificationSerializer
	permission_classes = [permissions.IsAuthenticated, IsLoggedUserNoSafeMethods]
	paginate_by = 7
	paginate_by_param = 'limit'
	max_paginate_by = 30

	def get_queryset(self):
		user = get_object_or_404(models.User.objects.all(), username=self.kwargs['username'])
		return models.Notification.objects.filter(user=user).order_by('-time').all()

class UserUnreadNotificationViewSet(viewsets.GenericViewSet,
							mixins.ListModelMixin):
	serializer_class = serializers.NotificationSerializer
	paginate_by = 7
	paginate_by_param = 'limit'
	max_paginate_by = 30

	def get_queryset(self):
		user = get_object_or_404(models.User.objects.all(), username=self.kwargs['username'])
		return models.Notification.objects.filter(user=user, read=False).order_by('-time').all()