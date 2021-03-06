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

class IsOwnedByCharacter(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return obj.owner.owner == request.user

class IsLoggedUser(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
		return view.kwargs.get('username', None) == request.user.username

class IsLoggedUserNoSafeMethods(permissions.BasePermission):
	def has_permission(self, request, view):
		username = view.kwargs.get('username', None)
		if username is None:
			return True
		
		return view.kwargs.get('username', None) == request.user.username

	def has_object_permission(self, request, view, obj):
		return obj.user == request.user
