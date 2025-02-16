from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="邮箱",
        max_length=32,
        widget=forms.EmailInput(attrs={"class": "input", "placeholder": "邮箱"}),
    )
    password = forms.CharField(
        label="密码",
        min_length=6,
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "密码"}),
    )

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(
        label="邮箱",
        max_length=32,
        widget=forms.EmailInput(attrs={"class": "input", "placeholder": "邮箱"}),
    )
    password = forms.CharField(
        label="密码",
        min_length=6,
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "密码"}),
    )
    password1 = forms.CharField(
        label="再次输入密码",
        min_length=6,
        widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "再次输入密码"}),
    )
    class Meta:
        model = User
        fields = ('email', 'password')

    def clean_email(self):
        """验证用户邮箱是否存在"""
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password1(self):
        """验证两次密码是否输入相同"""
        if self.cleaned_data.get('password') != self.cleaned_data.get('password1'):
            raise forms.ValidationError('两次密码输入不一致')
        return self.cleaned_data.get('password1')

class ForgetPwdForm(forms.Form):
    email = forms.EmailField(label="请输入注册邮箱地址", min_length=4, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))

class ModifyPwdForm(forms.Form):
    """修改密码"""
    password = forms.CharField(
        label="输入新密码",
        min_length=6,
        widget=forms.PasswordInput(
            attrs={"class": "input", "placeholder": "密码"}
        ),
    )

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
        }

class UserProfileForm(forms.ModelForm):
    """Form definition for UserInfo."""
    class Meta:
        """Meta definition for UserInfoform."""
        model = UserProfile
        fields = (
            "desc",
            "character",
            "birthday",
            "gender",
            "address",
            "image",
        )
        widgets = {
            "desc": forms.Textarea(attrs={"class": "input"}),
            "character": forms.TextInput(attrs={"class": "input"}),
            "birthday": forms.DateInput(attrs={"class": "input"}),
            "gender": forms.Select(attrs={"class": "input"}),
            "address": forms.TextInput(attrs={"class": "input"}),
            "image": forms.FileInput(attrs={"class": "input"}),
        }
