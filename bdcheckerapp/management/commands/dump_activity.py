# -*- coding: utf-8 -*-
"""
Usage:

managep.py activity_pk file_name

dumps Activity and all related grade parts to a json file.
"""
from django.core import serializers
from django.core.management import BaseCommand, CommandError
from django.db.models.query_utils import Q
from grading.models._models import GradeableActivity, AutogradeableGradePart, GradePart


class Command(BaseCommand):

    help = __doc__

    def handle(self, *args, **options):

        if len(args) != 2:
            raise CommandError("Need two arguments")

        pk = args[0]
        file_name = args[1]

        json_serializer = serializers.get_serializer("json")()

        with open(file_name, 'w') as str:
            activity = GradeableActivity.objects.get(pk = pk)
            agp = AutogradeableGradePart.objects.filter(activity=activity)
            grade_parts = list()
            ids = agp.values_list("pk")
            grade_parts.extend(GradePart.objects.filter(activity=activity))
            grade_parts.extend(agp)
            grade_parts.append(activity)
            json_serializer.serialize(grade_parts, stream=str)

