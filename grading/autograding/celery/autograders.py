# -*- coding: utf-8 -*-
from grading.autograding import OfflineAutograder
from grading.autograding.celery.tasks import DefaultAutograderTask


class CeleryAutograder(OfflineAutograder):

    TASK = DefaultAutograderTask

    def _apply_async_kwargs(self, **kwargs):
        kwargs['countdown'] = 3
        return kwargs

    def autograde_offline(self, current_grade, model_instance,
                          grading_result_model):
        task = self.TASK()
        if current_grade.pk is None or model_instance.pk is None or grading_result_model is None:
            raise ValueError()

        delayed = task.apply_async(
            **self._apply_async_kwargs(args=[
                current_grade.pk, model_instance.pk, grading_result_model.pk,
                self.NAME
            ])
        )

        grading_result_model.celery_task_id = delayed.task_id
        grading_result_model.save()
