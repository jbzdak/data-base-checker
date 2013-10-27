# -*- coding: utf-8 -*-
import abc

from celery import Task
from django.utils.translation import ugettext
from grading.models._models import GradePart, AutogradingResult, PartialGrade


class AutograderTask(Task):

    @abc.abstractmethod
    def perform_offilne_grading(
            self, current_grade, model_instance,
            grading_result_model, autograder):
        pass

    def run(self, current_grade, model_instance, grading_result_model, AutograderClass, *args, **kwargs):

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
        super().after_return(status, retval, task_id, args, kwargs, einfo)


class DefaultAutograderTask(AutograderTask):
    def perform_offilne_grading(self, current_grade, model_instance,
                                grading_result_model, autograder):
        return autograder.autograde(current_grade, model_instance)