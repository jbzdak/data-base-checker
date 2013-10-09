# -*- coding: utf-8 -*-
from grading.autograding import OfflineAutograder


class CeleryAutograder(OfflineAutograder):

    TASK = None

    def _apply_async_kwargs(self, **kwargs):
        kwargs['eta'] = 3
        return kwargs

    def autograde_offline(self, current_grade, model_instance,
                          grading_result_model):

        delayed = self.TASK.apply_async(
            **self._apply_async_kwargs(args=[
                current_grade.pk, model_instance.pk, grading_result_model.pk,
                type(self)
            ])
        )

        grading_result_model.celery_task_id = delayed.task_id

        grading_result_model.save()
