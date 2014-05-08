from rest_framework import permissions

class IsFromUser(permissions.BasePermission):
	"""
	If user A follows user B, then only user A can unfollow user B
	"""

	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return obj.from_user == request.user

class IsAuthor(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return obj.author == request.user

class IsOwner(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return obj.owner == request.user

class IsOwnerCharacter(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return obj.owner.owner == request.user