from rest_framework.generics import get_object_or_404
from rest_framework import permissions, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from socialbattle.api import models
from socialbattle.api import serializers
from socialbattle.api.permissions import IsOwnedByCharacter
from django.core.exceptions import ValidationError, ObjectDoesNotExist

### ITEM
# GET: /room/relax/{room_slug}/items/
# GET: /items/{item_slug}/
class ItemViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
	model = models.Item
	serializer_class = serializers.ItemSerializer
	lookup_field = 'slug'

class RoomItemViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		List of the available items for the chosen relax room
	'''
	serializer_class = serializers.ItemSerializer

	def get_queryset(self):
		queryset = models.Item.objects.all()
		room_slug = self.kwargs.get('room_slug')
		if room_slug:
			queryset = queryset.filter(relaxroom__slug=room_slug).all()
		return queryset


### INVENTORY
# GET, DELETE, PUT: /inventory/{pk}/
# GET: /characters/{character_name}/inventory/
class CharacterInventoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
	'''
		The inventory of the selected character.  
	'''
	serializer_class = serializers.InventoryRecordSerializer

	def get_queryset(self):
		queryset = models.InventoryRecord.objects.all()
		name = self.kwargs.get('character_name')
		if name:
			character = get_object_or_404(models.Character.objects.all(), name=name)
			queryset = queryset.filter(owner=character)
		return queryset

class InventoryRecordViewSet(viewsets.GenericViewSet,
							mixins.RetrieveModelMixin,
							mixins.UpdateModelMixin,
							mixins.DestroyModelMixin):
	'''
		Detailed view of an inventory record:
		It is possible to equip (`PUT`) items.  
		It is possible to use (`DELETE`) restorative items.
	'''
	queryset = models.InventoryRecord.objects.all()
	serializer_class = serializers.InventoryRecordSerializer
	permission_classes = [permissions.IsAuthenticated, IsOwnedByCharacter]

	def pre_save(self, obj):
		RESTORATIVE = models.Item.ITEM_TYPE[0][0]
		ARMOR = models.Item.ITEM_TYPE[2][0]
		WEAPON = models.Item.ITEM_TYPE[1][0]

		records = self.get_queryset().filter(owner=obj.owner).all()

		if obj.item.item_type == RESTORATIVE and obj.equipped == True:
			raise ValidationError({"msg": ["Cannot equip a restorative time"]})

		#automatically unequip the previous item
		if obj.item.item_type == ARMOR and obj.equipped == True:
			eq_armor = obj.owner.armor
			if eq_armor:
				eq_armor.equipped = False
				eq_armor.save()

		if obj.item.item_type == WEAPON and obj.equipped == True:
			eq_weapon = obj.owner.weapon
			if eq_weapon:
				eq_weapon.equipped = False
				eq_weapon.save()

	def destroy(self, request, *args, **kwargs):
		record = self.get_object()
		character = record.owner
		item = record.item

		if item.item_type != models.Item.ITEM_TYPE[0][0]:
			return Response({'msg': 'You can use only restorative items'}, status=status.HTTP_400_BAD_REQUEST)

		effect = item.get_restorative_effect(character)
		character.update_hp(-effect)
		record.quantity -= 1
		if record.quantity == 0:
			record.delete()
		else:
			record.save()
		data = {
				'effect': effect,
				'curr_hp': character.curr_hp,
				'inventory_record': self.get_serializer(record).data
			}
		return Response(data, status=status.HTTP_200_OK)