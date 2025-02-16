from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    """
    用户多关联的数据，可以见于http://127.0.0.1:8000/admin/auth/user/add/
    """
    USER_GENDER_TYPE = (
        ('male', '男'),
        ('female', '女')
    )
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    desc = models.TextField('个人简介', max_length=200, blank=True, default="")
    character = models.CharField('个性签名', max_length=100, blank=True, default="")
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    address = models.CharField(max_length=100, verbose_name='地址', default='', blank=True)
    gender = models.CharField(max_length=6, choices=USER_GENDER_TYPE, default='male', verbose_name='性别')
    image = models.ImageField(upload_to='images/%Y/%m', default='images/default.png', max_length=100, verbose_name='头像')

    class Meta:
        verbose_name = "用户数据"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.owner.username
    
class EmailVerifyRecord(models.Model):
    """邮箱验证码校验记录"""
    SEND_TYPE_CHOICES = (
        ('register', '注册'),
        ('forget', '找回密码')
    )
    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=35)
    send_type = models.CharField(choices=SEND_TYPE_CHOICES, default='register', max_length=20)

    class Meta:
        verbose_name = '邮箱验证码'
        # 复数形式
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
