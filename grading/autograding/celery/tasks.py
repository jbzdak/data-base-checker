# -*- coding: utf-8 -*-
import abc

from celery import Task
from django.db.transaction import atomic
from django.utils.translation import ugettext
from grading.autograding._base import get_autograders
from grading.models._models import GradePart, AutogradingResult, PartialGrade


class AutograderTask(Task):

    @abc.abstractmethod
    def perform_offilne_grading(
            self, current_grade, model_instance,
            grading_result_model, autograder):
        pass

    def run(self, current_grade, model_instance, grading_result_model, autograder_name, *args, **kwargs):

        with atomic():
            AutograderClass = get_autograders()[autograder_name]
            autograder = AutograderClass()
            current_grade = PartialGrade.objects.get(pk = current_grade)
            model_instance = autograder.SubmissionModel.objects.get(pk=model_instance)
            grading_result_model = AutogradingResult.objects.get(pk=grading_result_model)
            grading_result = self.perform_offilne_grading(
                current_grade, model_instance,
                grading_result_model, autograder)
            grading_result_model.fill(model_instance, grading_result)
            grading_result_model.save()

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        if status == 'FAILURE':
            agr = AutogradingResult.objects.get(pk=args[2])
            agr.fill_grading_failed()
            agr.save()

class DefaultAutograderTask(AutograderTask):
    def perform_offilne_grading(self, current_grade, model_instance,
                                grading_result_model, autograder):
        return autograder.autograde(current_grade, model_instance)