from django.contrib import admin
from django.contrib.auth.models import User
# 继承UserAdmin可以注册到管理后台
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, EmailVerifyRecord

# Register your models here.

# 取消关联注册User
admin.site.unregister(User)

# 定义关联对象的样式，StackedInline为纵向，TabularInline为横向
class UserProfileInline(admin.StackedInline):
    model = UserProfile # 关联的模型

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline] # 将UserProfileInline注册到UserAdmin中

# 重新关联注册User
admin.site.register(User, UserProfileAdmin)

# 注册邮箱验证
@admin.register(EmailVerifyRecord)
class Admin(admin.ModelAdmin):
    """admin view for"""
    list_display = ('code',)