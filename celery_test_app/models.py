from django.db import models

# Create your models here.
from grading.autograding import OfflineAutograder


class InputAutograder(OfflineAutograder):
    def autograde_offline(self, current_grade, model_instance,
                          grading_result_model):
        super().autograde_offline(current_grade, model_instance,
                                  grading_result_model)