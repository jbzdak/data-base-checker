# -*- coding: utf-8 -*-

import string, random

from django.contrib.auth.models import User
from grading.models._models import Student


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for x in range(size))

def create_student(course = None):
    user = User.objects.create(username=id_generator(10))
    student = Student.objects.create(user=user)
    if course is not None:
        student.course = course
        student.save()
    return user, student