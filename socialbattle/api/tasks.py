from __future__ import absolute_import

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from socialbattle.api.models import InventoryRecord
from socialbattle.api import mechanics
from socialbattle.api.serializers import NotificationSerializer, PostGetSerializer, CommentSerializer
import random, time

@shared_task
def end_battle(character, mob):
	# add dropped items
	drops = list(mob.drops.all())
	for item in drops:
		try:
			record = InventoryRecord.objects.get(owner=character, item=item)
			record.quantity += 1
			record.save()
		except ObjectDoesNotExist:
			record = InventoryRecord.objects.create(
						owner=character,
						item=item, 
					)

	#update aps, guils, exp and level
	character.ap += mob.ap
	character.guils += mob.guils
	character.exp += mob.exp
	diff_level = 0
	while character.exp >= mechanics.get_exp(character.level + 1):
		character.level += 1
		diff_level += 1

	#update stats
	if diff_level > 0:
		character.max_hp = mechanics.get_stat(character.level, 'HP')
		character.max_mp = mechanics.get_stat(character.level, 'MP')
		character.stre = mechanics.get_stat(character.level, 'STR')
		character.spd = mechanics.get_stat(character.level, 'SPD')
		character.mag = mechanics.get_stat(character.level, 'MAG')
		character.vit = mechanics.get_stat(character.level, 'VIT')

	character.save()

@shared_task
def apply_exchange(offerer, acceptor, post):
	exchanges = list(post.exchanged_items.all())
	for exchange in exchanges:
		if exchange.given:
			offerer.remove_from_inventory(exchange)
			acceptor.add_to_inventory(exchange)
		else:
			acceptor.remove_from_inventory(exchange)
			offerer.add_to_inventory(exchange)

	offerer.guils -= post.give_guils
	acceptor.guils += post.give_guils
	acceptor.guils -= post.receive_guils
	offerer.guils += post.receive_guils

	acceptor.save()
	offerer.save()

from socialbattle.api import pusher
from socialbattle.api.models import Activity, Notification

@shared_task
def notify_followers(user, event, data, create=False):
	followers = list(user.followers.all())
	if followers:
		if create:
			activity = Activity.objects.create(data=data, event=event)

		for f in followers:
			if create:
				n = Notification.objects.create(user=f, activity=activity)
				data['id'] = n.pk

			pusher[f.username].trigger(event, data)

@shared_task
def notify_user(user, event, data, create=False):
	if create:
		activity = Activity.objects.create(data=data, event=event)
		n = Notification.objects.create(user=user, activity=activity)
		data['id'] = n.pk

	pusher[user.username].trigger(event, data)

@shared_task
def notify_commentors(user, post, data, event, create=False):
	commentors = [comment.author for comment in post.comment_set.all()]
	commentors = set(filter((lambda c: c != post.author and c != user), commentors))

	if commentors:
		if create:
			activity = Activity.objects.create(data=data, event=event)
		

		for commentor in commentors:
			if create:
				n = Notification.objects.create(user=commentor, activity=activity)
				data['id'] = n.pk

			pusher[commentor.username].trigger(event, data)

#room channels
@shared_task
def push_comment(comment, post_id):
	pusher['post-%d' % post_id].trigger('new-comment', comment)

@shared_task
def push_post(post):
	pusher[post['room']['slug']].trigger('new-post', post)