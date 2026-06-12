import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from .forms import RegisterForm, LoginForm, ProfileEditForm, ChangePasswordForm
from .models import Skill

User = get_user_model()


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("projects:project_list")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            username=form.cleaned_data["email"], password=form.cleaned_data["password"]
        )
        if user:
            login(request, user)
            return redirect("projects:project_list")
        form.add_error(None, "Неверный имейл или пароль")
    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:project_list")


def user_details(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    return render(request, "users/user-details.html", {"user_obj": user_obj})


def participants_list(request):
    skill_filter = request.GET.get("skill")
    if skill_filter:
        users_qs = User.objects.filter(
            skills__name=skill_filter, is_active=True
        ).order_by("id")
    else:
        users_qs = User.objects.filter(is_active=True).order_by("id")

    paginator = Paginator(users_qs, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    all_skills = Skill.objects.all().order_by("name")

    return render(
        request,
        "users/participants.html",
        {
            "participants": page_obj,
            "all_skills": all_skills,
            "active_skill": skill_filter,
        },
    )


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:user_details", pk=request.user.pk)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if request.user.check_password(form.cleaned_data["old_password"]):
                if (
                    form.cleaned_data["new_password1"]
                    == form.cleaned_data["new_password2"]
                ):
                    request.user.set_password(form.cleaned_data["new_password1"])
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    return redirect("users:user_details", pk=request.user.pk)
                form.add_error("new_password2", "Пароли не совпадают")
            else:
                form.add_error("old_password", "Неверный старый пароль")
    else:
        form = ChangePasswordForm()
    return render(request, "users/change_password.html", {"form": form})


def skills_search(request):
    q = request.GET.get("q", "")
    skills = Skill.objects.filter(name__icontains=q).order_by("name")[:10]
    return JsonResponse([{"id": s.id, "name": s.name} for s in skills], safe=False)


@login_required
@require_POST
def add_skill(request, pk):
    if request.user.pk != int(pk):
        return JsonResponse({"added": False}, status=403)

    skill_id = request.POST.get("skill_id")
    name = request.POST.get("name")
    created = False

    if skill_id:
        skill = get_object_or_404(Skill, pk=skill_id)
    elif name:
        skill, created = Skill.objects.get_or_create(name=name.strip())
    else:
        return JsonResponse({"added": False}, status=400)

    if skill in request.user.skills.all():
        return JsonResponse({"skill_id": skill.id, "created": created, "added": False})

    request.user.skills.add(skill)
    return JsonResponse({"skill_id": skill.id, "created": created, "added": True})


@login_required
@require_POST
def remove_skill(request, pk, skill_id):
    if request.user.pk != int(pk):
        return JsonResponse({"removed": False}, status=403)
    user_obj = get_object_or_404(User, pk=pk)
    skill = get_object_or_404(Skill, pk=skill_id)
    if skill in user_obj.skills.all():
        user_obj.skills.remove(skill)
        return JsonResponse({"removed": True})
    return JsonResponse({"removed": False})
