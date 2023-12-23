# analysis_app/models.py
from django.db import models


class ExpertOpinion(models.Model):
    opinion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.opinion


