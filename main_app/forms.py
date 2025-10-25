from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Allergy
from .models import Profile


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False, max_length=30, label=_('First name'))
    last_name = forms.CharField(required=False, max_length=150, label=_('Last name'))

    class Meta:
        model = Profile
        fields = ['age', 'avatar']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # populate initial user fields
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        # save user fields
        user = getattr(profile, 'user', None)
        if user:
            user.first_name = self.cleaned_data.get('first_name', user.first_name)
            user.last_name = self.cleaned_data.get('last_name', user.last_name)
            if commit:
                user.save()
        if commit:
            profile.save()
        return profile


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=False, max_length=30, label=_('First name'))
    last_name = forms.CharField(required=False, max_length=150, label=_('Last name'))
    username = forms.CharField(label=_('Username'))
    email = forms.EmailField(required=True, label=_('Email'))
    age = forms.IntegerField(required=False, min_value=0, max_value=150, label=_('Age'))
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)


    class Meta:
        model = User
        
        fields = ['first_name', 'last_name', 'username', 'email', 'age', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()


            age = self.cleaned_data.get('age')
            if age is not None:

                from .models import Profile
                p, _ = Profile.objects.get_or_create(user=user)
                p.age = age
                p.save()


        return user

    def clean_email(self):
        """Ensure the provided email address is not already used by another account.

        This performs a case-insensitive check against existing users and raises
        a ValidationError when a duplicate is found.
        """
        email = self.cleaned_data.get('email')
        if email:
            # Case-insensitive match
            if User.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError("A user with that email address already exists.")
        return email
