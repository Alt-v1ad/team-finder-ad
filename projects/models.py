from django.conf import settings
from django.db import models
from django.urls import reverse

from .constants import PROJECT_NAME_MAX_LEN, PROJECT_STATUS_MAX_LEN, ProjectStatus


class Project(models.Model):
    name = models.CharField(max_length=PROJECT_NAME_MAX_LEN)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    github_url = models.URLField(blank=True, null=True)
    status = models.CharField(
        max_length=PROJECT_STATUS_MAX_LEN,
        choices=ProjectStatus.CHOICES,
        default=ProjectStatus.OPEN,
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="participated_projects", blank=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("projects:project_details", kwargs={"pk": self.pk})
