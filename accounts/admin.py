from django.contrib import admin

# Register your models here.
from django import forms
from django.contrib.auth.admin import UserAdmin

from accounts.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username')

    def save(self, commit):
        user = super().save(commit=False)
        user.set_passwrod(self.cleaned_data['password'])
        if commit:
            user.save()
            return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'username')


admin.site.register(User)