from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("list/", views.participants_list, name="participants_list"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("skills/", views.skills_search, name="skills_search"),
    path("<int:pk>/", views.user_details, name="user_details"),
    path("<int:pk>/skills/add", views.add_skill, name="add_skill"),
    path(
        "<int:pk>/skills/<int:skill_id>/remove/",
        views.remove_skill,
        name="remove_skill",
    ),
]
