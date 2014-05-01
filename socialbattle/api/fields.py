from rest_framework.serializers import HyperlinkedIdentityField
from rest_framework.reverse import reverse

class NestedHyperlinkedIdentityField(HyperlinkedIdentityField):
	lookup_fields = None

	def __init__(self, *args, **kwargs):
		self.lookup_fields = kwargs.pop('lookup_fields', None)
		super(NestedHyperlinkedIdentityField, self).__init__(*args, **kwargs)

	def get_url(self, obj, view_name, request, format):
		if not self.lookup_fields:
			return None

		kwargs = {}
		for lookup_field in self.lookup_fields:
			kwargs[lookup_field] = getattr(obj, lookup_field, None)
		
		return reverse(view_name, kwargs=kwargs, request=request, format=format)