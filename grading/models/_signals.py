# coding=utf-8

import logging

from django.db.utils import ProgrammingError

from grading.models._models import *

LOGGER = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def on_user_create(instance, **kwargs):
    try:
        Student.objects.create(user=instance)
    except ProgrammingError as e:
        print(e.message)
        if "does not exist" in e.args[0] and 'grading_student' in e.args[0]:
            LOGGER.warning("Adding user before tables for grading subsystem. Student model was not installed for this user.")


@receiver(pre_save)
def on_gradeable_activity_create(instance, **kwargs):
    if isinstance(instance, NamedSortable) and not instance.sort_key:
        instance.sort_key = instance.name
