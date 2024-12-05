from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import User
from qa.models import Answer


@receiver(m2m_changed, sender=Answer.likes.through)
def update_likes_count(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.author.update_like_count()


@receiver(m2m_changed, sender=Answer.dislikes.through)
def update_dislikes_count(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.author.update_dislike_count()


@receiver(post_save, sender=Answer)
def update_accepted_count(sender, instance, created, **kwargs):
    if not created and 'is_correct' in instance.changed_data:
        instance.author.update_accepted_count()
