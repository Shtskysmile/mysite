from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import (
    LoginForm,
    RegisterForm,
    ForgetPwdForm,
    ModifyPwdForm,
    UserForm,
    UserProfileForm,
)
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from .models import EmailVerifyRecord, UserProfile
from utils.email_send import send_register_email
from django.contrib.auth.decorators import login_required


# Create your views here.
class MyBackend(ModelBackend):
    """邮箱登录注册"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def active_user(request, active_code):
    """修改用户状态，比对验证码"""
    all_records = EmailVerifyRecord.objects.filter(code=active_code)
    if all_records:
        for record in all_records:
            email = record.email
            user = User.objects.get(email=email)
            user.is_staff = True
            user.save()
    else:
        return HttpResponse("链接有误")

    return redirect("users:login")


def login_view(request):
    if request.method != "POST":
        form = LoginForm()

    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("users:user_profile")
            else:
                return HttpResponse("登陆失败")

    context = {"form": form}
    return render(request, "users/login.html", context)


def register_view(request):
    """注册试图"""
    if request.method != "POST":
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            # 把密码转换为Hash值
            new_user.set_password(form.cleaned_data.get("password"))
            new_user.username = form.cleaned_data.get("email")
            new_user.save()
            # 发送邮件
            send_register_email(form.cleaned_data.get("email"), "register")
            return HttpResponse("注册成功")

    context = {"form": form}
    return render(request, "users/register.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")


def forget_pwd(request):
    if request.method == "GET":
        form = ForgetPwdForm()

    else:
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            exists = User.objects.filter(email=email).exists()
            if exists:
                # 发送邮件
                send_register_email(email, "forget")
                return HttpResponse("邮件已经发送请查收!")

            else:
                return HttpResponse("邮箱还未注册，请前往注册!")

    return render(request, "users/forget_pwd.html", {"form": form})


def forget_pwd_url(request, active_code):
    if request.method != "POST":
        form = ModifyPwdForm()

    else:
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            record = EmailVerifyRecord.objects.get(code=active_code)
            email = record.email
            user = User.objects.get(email=email)
            user.username = email
            user.password = make_password(form.cleaned_data.get("password"))
            user.save()
            return HttpResponse("修改成功")
        else:
            return HttpResponse("修改失败")

    return render(request, "users/reset_pwd.html", {"form": form})


@login_required(login_url="user:login")
def user_profile(request):
    user = User.objects.get(username=request.user)
    return render(request, "users/user_profile.html", {"user": user})


@login_required(login_url="user:login")
def editor_users(request):
    """编辑用户信息"""
    # 获取当前用户
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        try:
            user_profile = user.userprofile
            # 默认显示原有的数据
            form = UserForm(request.POST, instance=user)
            # 用户提交的信息
            user_profile_form = UserProfileForm(
                request.POST, request.FILES, instance=user_profile
            )

        except UserProfile.DoesNotExist:
            # 默认显示原有的数据
            form = UserForm(request.POST, instance=user)
            # 用户提交的信息
            user_profile_form = UserProfileForm(request.POST, request.FILES)

        finally:
            print(form.is_valid(), user_profile_form.is_valid())
            if form.is_valid() and user_profile_form.is_valid():
                form.save()
                new_user_profile = user_profile_form.save(commit=False)
                new_user_profile.owner = request.user
                new_user_profile.save()
                return redirect("users:user_profile")

    else:
        try:
            # 如果这里为None(第一次登录时候)，下面的代码会进入异常处理
            user_profile = user.userprofile
            # 默认显示原有的数据
            form = UserForm(instance=user)
            # 用户提交的信息
            user_profile_form = UserProfileForm(instance=user_profile)

        except UserProfile.DoesNotExist:
            # 默认显示原有的数据
            form = UserForm(instance=user)
            # 用户提交的信息
            user_profile_form = UserProfileForm()

    return render(
        request,
        "users/editor_users.html",
        {"form": form, "user_profile_form": user_profile_form},
    )
