# coding=utf-8

from grading.models._models import *

@receiver(post_save, sender=User)
def on_user_create(instance, **kwargs):
    Student.objects.create(user=instance)



@receiver(pre_save)
def on_gradeable_activity_create(instance, **kwargs):
    if isinstance(instance, NamedSortable) and not instance.sort_key:
        instance.sort_key = instance.name
