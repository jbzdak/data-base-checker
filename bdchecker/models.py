

from django.db import models
from grading.models import GradePart, GradeableActivity

from verifiers import get_verifiers

part_types = (
    (1, "submit_file"),
    (2, "submit_text"),
    (3, "submit_sql")
)

class BDCheckerActivity(GradeableActivity):

    class Meta:
        proxy = True
        app_label = "bdchecker"

class BDCheckerGradePart(GradePart):

    parent = models.OneToOneField("grading.GradePart", parent_link=True, related_name="bdchecker_part")

    part_type = models.SmallIntegerField(choices=part_types)
    verifier_name = models.CharField(
        choices=[(name, name) for name in get_verifiers().keys()],
        max_length=1000)

    class Meta:
        app_label = "bdchecker"
        ordering = ("sort_key",)
