import random
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=124, unique=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=12)
    github_url = models.URLField(blank=True, null=True)
    about = models.TextField(max_length=256, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    skills = models.ManyToManyField(Skill, related_name="users", blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname", "phone"]

    def save(self, *args, **kwargs):
        # Автогенерация аватарки с первой буквой имени
        if not self.avatar and self.name:
            img = Image.new(
                "RGB",
                (200, 200),
                color=(
                    random.randint(50, 200),
                    random.randint(50, 200),
                    random.randint(50, 200),
                ),
            )
            d = ImageDraw.Draw(img)
            d.text((80, 80), self.name[0].upper(), fill=(255, 255, 255))
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            self.avatar.save(
                f"avatar_{self.email}.png", ContentFile(buffer.getvalue()), save=False
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"
