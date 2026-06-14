from django import forms


class GitHubUrlValidatorMixin:
    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        if url and "github.com" not in url:
            raise forms.ValidationError("Ссылка должна вести на профиль GitHub.")
        return url
