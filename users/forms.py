from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone", "country", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["placeholder"] = field.label

            self.fields["phone"].required = False
            self.fields["country"].required = False

    def clean_email(self):
        """Проверка email на уникальность"""
        email = self.cleaned_data.get("email")
        email = email.lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(f"Пользователь с {email} уже существует")
        return email

    def clean_password1(self):
        """Проверка длины пароля"""
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise ValidationError("Пароль должен состоять минимум из 8 символов")
        return password


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "phone", "country", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].disabled = True
        self.fields["avatar"].widget.attrs["class"] = "form-control-file"
