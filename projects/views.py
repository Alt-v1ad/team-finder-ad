from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from team_finder.services import get_paginated_page

from .constants import PAGINATION_LIMIT, ProjectStatus
from .forms import ProjectForm
from .models import Project


def project_list(request):
    projects_qs = (
        Project.objects.select_related("owner")
        .prefetch_related("participants")
        .order_by("-created_at")
    )
    page_obj = get_paginated_page(request, projects_qs, PAGINATION_LIMIT)
    return render(request, "projects/project_list.html", {"projects": page_obj})


def project_details(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def create_project(request):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect("projects:project_details", pk=project.pk)
    return render(
        request, "projects/create-project.html", {"form": form, "is_edit": False}
    )


@login_required
def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect("projects:project_details", pk=project.pk)
    return render(
        request, "projects/create-project.html", {"form": form, "is_edit": True}
    )


@login_required
@require_POST
def complete_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)
    if project.status == ProjectStatus.OPEN:
        project.status = ProjectStatus.CLOSED
        project.save()
        return JsonResponse({"status": "ok", "project_status": ProjectStatus.CLOSED})
    return JsonResponse({"status": "error"}, status=HTTPStatus.BAD_REQUEST)


@login_required
@require_POST
def toggle_participate(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.participants.filter(pk=request.user.pk).exists():
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)
    return JsonResponse({"status": "ok"})
