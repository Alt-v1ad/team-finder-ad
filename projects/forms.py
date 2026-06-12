from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Project.STATUS_CHOICES, widget=forms.Select)

    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        if url and "github.com" not in url:
            raise forms.ValidationError("Ссылка должна вести на GitHub.")
        return url
