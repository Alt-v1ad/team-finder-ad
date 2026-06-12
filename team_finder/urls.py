from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def redirect_to_projects(request):
    return redirect("projects:project_list")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", redirect_to_projects, name="root_redirect"),
    path("users/", include("users.urls", namespace="users")),
    path("project/", include("projects.urls", namespace="projects")),
    path("projects/", include("projects.urls", namespace="projects_alt")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
