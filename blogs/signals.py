from django.db.models.signals import post_save
from django.dispatch import receiver

from blogs.models import BlogPost, Notification, Comment
from general.functions import get_auto_id


def create_notification(sender, instance, created, **kwargs):
    post_author = instance.post.creator
    if post_author != instance.creator:

        Notification.objects.create(
            creator = instance.creator,
            updater = instance.creator,
            auto_id = get_auto_id(Comment),

            user=post_author, 
            comment=instance, 
        )

        print("Notification created")
    else:
        print("Same Author")


# Connect the signal to the Comment model's post_save signal
post_save.connect(create_notification, sender=Comment)
