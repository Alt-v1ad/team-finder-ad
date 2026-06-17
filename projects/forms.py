from django import forms

from team_finder.mixins import GitHubUrlValidatorMixin

from .constants import ProjectStatus
from .models import Project


class ProjectForm(GitHubUrlValidatorMixin, forms.ModelForm):
    status = forms.ChoiceField(choices=ProjectStatus.CHOICES, widget=forms.Select)

    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
