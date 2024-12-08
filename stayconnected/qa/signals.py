from django.db.models.signals import post_save
from django.dispatch import receiver
from qa.models import Answer


@receiver(post_save, sender=Answer)
def update_question_completion(sender, instance, **kwargs):
    if instance.is_correct:
        instance.question.check_completion()
