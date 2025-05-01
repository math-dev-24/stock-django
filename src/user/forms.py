from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django import forms


class UserLoginForm(AuthenticationForm):
    """Formulaire pour l'authentification des utilisateurs existants"""
    input_classes = "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': input_classes,
                'placeholder': "Nom d'utilisateur",
                'autofocus': True
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': input_classes,
                'placeholder': 'Mot de passe'
            }
        )
    )

    error_messages = {
        'invalid_login': "Veuillez entrer un nom d'utilisateur et un mot de passe corrects. "
                         "Notez que les deux champs peuvent être sensibles à la casse.",
        'inactive': "Ce compte est inactif.",
    }

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = self.input_classes


class UserSignup(UserCreationForm):
    """Formulaire pour la création de nouveaux utilisateurs"""
    input_classes = "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': input_classes,
                'placeholder': "Choisissez un nom d'utilisateur"
            }
        )
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': input_classes,
                'placeholder': 'Votre adresse email'
            }
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': input_classes,
                'placeholder': 'Créez un mot de passe'
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': input_classes,
                'placeholder': 'Confirmez votre mot de passe'
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = self.input_classes

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("L'adresse email est obligatoire.")

        user = get_user_model()
        if user.objects.filter(email=email).exists():
            raise ValidationError("Cette adresse email est déjà utilisée.")

        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError("Le nom d'utilisateur est obligatoire.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not password1:
            self.add_error('password1', "Le mot de passe est obligatoire.")

        if not password2:
            self.add_error('password2', "La confirmation du mot de passe est obligatoire.")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Les mots de passe ne correspondent pas.")

        return cleaned_data