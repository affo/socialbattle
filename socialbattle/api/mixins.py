from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import status

#it seems strange but the create mixin doesn't handle the permissions to create
class CreateWithPermissionModelMixin(CreateModelMixin):
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.DATA, files=request.FILES)
		if serializer.is_valid():
			obj = serializer.object
			self.check_object_permissions(request, obj)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

		return super(CreateWithPermissionModelMixin, self).create(request, *args, **kwargs)