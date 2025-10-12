from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Allergy


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=False, max_length=30)
    last_name = forms.CharField(required=False, max_length=150)
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=False, min_value=0, max_value=150)


    class Meta:
        model = User
       
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

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
