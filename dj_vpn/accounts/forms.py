from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AdminUserCreationForm


user = get_user_model()


class AdminUserChangeForm(forms.ModelForm):
    password = forms.CharField(widget=forms.TextInput, label="password")

    class Meta:
        model = user
        fields = "__all__"


class UserAccountCreationForm(AdminUserCreationForm):
    password1 = forms.CharField(widget=forms.TextInput, label="password")
    password2 = forms.CharField(widget=forms.TextInput, label="password_confirm")

    class Meta(UserCreationForm):
        model = user
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def validate_password_for_user(self, user, **kwargs):
        pass
