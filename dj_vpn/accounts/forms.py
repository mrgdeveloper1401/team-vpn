from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, SetUnusablePasswordMixin, SetPasswordMixin
from django.contrib.auth.forms import AdminUserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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


class UserSetPasswordMixin(SetPasswordMixin):
    """
        Form mixin that validates and sets a password for a user.
        """

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }

    @staticmethod
    def create_password_fields(label1=_("Password"), label2=_("Password confirmation")):
        password1 = forms.CharField(
            label=label1,
            required=False,
            strip=False,
            widget=forms.TextInput(),
            # help_text= password_validation.password_validators_help_text_html(),
        )
        password2 = forms.CharField(
            label=label2,
            required=False,
            widget=forms.TextInput(),
            strip=False,
            help_text=_("Enter the same password as before, for verification."),
        )
        return password1, password2

    def validate_passwords(
            self,
            password1_field_name="password1",
            password2_field_name="password2",
    ):
        password1 = self.cleaned_data.get(password1_field_name)
        password2 = self.cleaned_data.get(password2_field_name)

        if not password1 and password1_field_name not in self.errors:
            error = ValidationError(
                self.fields[password1_field_name].error_messages["required"],
                code="required",
            )
            self.add_error(password1_field_name, error)

        if not password2 and password2_field_name not in self.errors:
            error = ValidationError(
                self.fields[password2_field_name].error_messages["required"],
                code="required",
            )
            self.add_error(password2_field_name, error)

        if password1 and password2 and password1 != password2:
            error = ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
            self.add_error(password2_field_name, error)

    def validate_password_for_user(self, user, password_field_name="password2"):
        pass

    def set_password_and_save(self, user, password_field_name="password1", commit=True):
        user.set_password(self.cleaned_data[password_field_name])
        if commit:
            user.save()
        return user


class UserAdminPasswordChangeForm(SetUnusablePasswordMixin, UserSetPasswordMixin, forms.Form):
    """
      A form used to change the password of a user in the admin interface.
      """

    required_css_class = "required"
    usable_password_help_text = SetUnusablePasswordMixin.usable_password_help_text + (
        '<ul id="id_unusable_warning" class="messagelist"><li class="warning">'
        "If disabled, the current password for this user will be lost.</li></ul>"
    )
    password1, password2 = UserSetPasswordMixin.create_password_fields()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["autofocus"] = True
        if self.user.has_usable_password():
            self.fields["usable_password"] = (
                SetUnusablePasswordMixin.create_usable_password_field(
                    self.usable_password_help_text
                )
            )

    def clean(self):
        self.validate_passwords()
        self.validate_password_for_user(self.user)
        return super().clean()

    def save(self, commit=True):
        """Save the new password."""
        return self.set_password_and_save(self.user, commit=commit)

    @property
    def changed_data(self):
        data = super().changed_data
        if "set_usable_password" in data or "password1" in data and "password2" in data:
            return ["password"]
        return []


class CustomAdminLoginForm(AdminAuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)  # بررسی‌های پیش‌فرض (مثل is_staff, is_active)

        if user.is_superuser is False:
            if user.account_type != "premium_user":
                raise ValidationError(
                    "فقط کاربران پرمیوم اجازه دسترسی به پنل ادمین رو دارند",
                    code="invalid_login",
                )