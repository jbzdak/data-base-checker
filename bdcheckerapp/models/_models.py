
from django.db import models
from django.db.models.query_utils import Q
__all__= ['Team']

class TeamManager(models.Manager):

    def get_team_for_student(self, student, activity):
        try:
            return Team.objects.get(
                Q(student_1=student) | Q(student_2=student), activity=activity
            )
        except Team.DoesNotExist:
            return None

    def all_teams_for_student(self, student):
        return Team.objects.filter(Q(student_1=student) | Q(student_2=student))

    def get_other_student(self, student, activity):
        team = self.get_team_for_student(student, activity)

        if team is None:
            return None

        if student == team.student_1:
            return team.student_2
        return team.student_1


class Team(models.Model):
    activity = models.ForeignKey("grading.GradeableActivity")
    student_1 = models.ForeignKey("grading.Student", related_name="+")
    student_2 = models.ForeignKey("grading.Student", related_name="+")

    objects = TeamManager()

    class Meta:
        unique_together = [
            ['activity', 'student_1'],
            ['activity', 'student_2']
        ]
        app_label = "bdcheckerapp"
