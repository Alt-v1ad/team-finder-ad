import random
from io import BytesIO

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from PIL import Image, ImageDraw

from .constants import (
    ABOUT_MAX_LEN,
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
    AVATAR_TEXT_POS,
    PHONE_MAX_LEN,
    SKILL_NAME_MAX_LEN,
    USER_NAME_MAX_LEN,
)
from .managers import UserManager


class Skill(models.Model):
    name = models.CharField(max_length=SKILL_NAME_MAX_LEN, unique=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=USER_NAME_MAX_LEN)
    surname = models.CharField(max_length=USER_NAME_MAX_LEN)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=PHONE_MAX_LEN)
    github_url = models.URLField(blank=True, null=True)
    about = models.TextField(max_length=ABOUT_MAX_LEN, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    skills = models.ManyToManyField(Skill, related_name="users", blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "phone"]

    def save(self, *args, **kwargs):
        if not self.avatar and self.name:
            img = Image.new(
                "RGB",
                AVATAR_SIZE,
                color=tuple(random.randint(50, 200) for _ in range(3)),
            )
            d = ImageDraw.Draw(img)
            d.text(AVATAR_TEXT_POS, self.name[0].upper(), fill=AVATAR_TEXT_COLOR)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            self.avatar.save(
                f"avatar_{self.email}.png", ContentFile(buffer.getvalue()), save=False
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"

    def get_absolute_url(self):
        return reverse("users:user_details", kwargs={"pk": self.pk})
