# -*- coding: utf-8 -*-
import abc

from celery import Task
from grading.models._models import GradePart, AutogradingResult


class AutograderTask(Task):

    @abc.abstractmethod
    def perform_offilne_grading(
            self, current_grade, model_instance,
            grading_result_model, autograder):
        pass

    def run(self, current_grade, model_instance, grading_result_model, AutograderClass, *args, **kwargs):
        autograder = AutograderClass()
        current_grade = GradePart.objects.get(pk = current_grade)
        model_instance = autograder.SubmissionModel.objects.get(pk=model_instance)
        grading_result_model = AutogradingResult.objects.get(pk=grading_result_model)
        grading_result = self.perform_offilne_grading(
            current_grade, model_instance,
            grading_result_model, autograder)
        grading_result.fill(model_instance, grading_result)
        grading_result.save()

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        super().after_return(status, retval, task_id, args, kwargs, einfo)


