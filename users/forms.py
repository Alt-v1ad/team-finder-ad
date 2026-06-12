from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["name", "surname", "email", "password", "phone"]


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "avatar", "about", "phone", "github_url"]

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if not phone:
            return phone
        if (
            not (phone.startswith("8") or phone.startswith("+7"))
            or not phone.replace("+", "").isdigit()
        ):
            raise forms.ValidationError("Неверный формат телефона.")

        normalized = "+7" + phone[1:] if phone.startswith("8") else phone
        qs = User.objects.filter(phone=phone).exclude(pk=self.instance.pk)
        qs_norm = (
            User.objects.filter(phone="+7" + phone[1:]).exclude(pk=self.instance.pk)
            if phone.startswith("8")
            else User.objects.filter(phone="8" + phone[2:]).exclude(pk=self.instance.pk)
        )

        if qs.exists() or qs_norm.exists():
            raise forms.ValidationError("Этот номер телефона уже используется.")
        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        if url and "github.com" not in url:
            raise forms.ValidationError("Ссылка должна вести на профиль GitHub.")
        return url


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)
