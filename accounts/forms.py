from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Profile, DIRECTION_VALUES

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Nom d'utilisateur"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"}))


class ProfileForm(forms.ModelForm):
    """Formulaire édition profil — direction en liste déroulante."""
    direction = forms.ChoiceField(
        choices=[("", "— Sélectionner une direction —")] + DIRECTION_VALUES,
        required=False,
        label="Direction",
    )

    class Meta:
        model = Profile
        fields = ("role", "direction", "telephone")

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        direction = cleaned.get("direction", "").strip()
        if role in Profile.ROLES_AVEC_DIRECTION and not direction:
            raise ValidationError("La direction est obligatoire pour un Déclarant ou Chef de direction.")
        return cleaned


class UserCreateForm(forms.ModelForm):
    """Formulaire création utilisateur par la direction des risques."""
    password   = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")
    role       = forms.ChoiceField(choices=Profile.ROLE_CHOICES, label="Rôle")
    direction  = forms.ChoiceField(
        choices=[("", "— Sélectionner une direction —")] + DIRECTION_VALUES,
        required=False,
        label="Direction",
    )
    telephone  = forms.CharField(max_length=50, required=False, label="Téléphone")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        direction = cleaned.get("direction", "").strip()
        if role in Profile.ROLES_AVEC_DIRECTION and not direction:
            raise ValidationError("La direction est obligatoire pour un Déclarant ou Chef de direction.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            p = user.profile
            p.role      = self.cleaned_data["role"]
            p.direction = self.cleaned_data.get("direction", "")
            p.telephone = self.cleaned_data.get("telephone", "")
            p.save()
        return user


class UserEditForm(forms.ModelForm):
    """Formulaire édition d'un utilisateur existant (pas de mot de passe)."""
    role      = forms.ChoiceField(choices=Profile.ROLE_CHOICES, label="Rôle")
    direction = forms.ChoiceField(
        choices=[("", "— Sélectionner une direction —")] + DIRECTION_VALUES,
        required=False,
        label="Direction",
    )
    telephone = forms.CharField(max_length=50, required=False, label="Téléphone")

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        if profile:
            self.fields["role"].initial      = profile.role
            self.fields["direction"].initial = profile.direction
            self.fields["telephone"].initial = profile.telephone

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        direction = cleaned.get("direction", "").strip()
        if role in Profile.ROLES_AVEC_DIRECTION and not direction:
            raise ValidationError("La direction est obligatoire pour un Déclarant ou Chef de direction.")
        return cleaned

    def save_profile(self, profile):
        profile.role      = self.cleaned_data["role"]
        profile.direction = self.cleaned_data.get("direction", "")
        profile.telephone = self.cleaned_data.get("telephone", "")
        profile.save()
