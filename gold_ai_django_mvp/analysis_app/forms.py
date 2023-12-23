# analysis_app/forms.py
from django import forms
from .models import ExpertOpinion


class ExpertOpinionForm(forms.ModelForm):
    class Meta:
        model = ExpertOpinion
        fields = ['opinion']

