from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Student(models.Model):

    user = models.ForeignKey("auth.User")
    group = models.ForeignKey("StudentGroup", related_name="students", null=True, blank=True)


class StudentGroup(models.Model):

    name = models.CharField("Group name", max_length=100)

@receiver(post_save, sender=User)
def on_user_create(instance, **kwargs):
    Student.objects.create(user=instance)


