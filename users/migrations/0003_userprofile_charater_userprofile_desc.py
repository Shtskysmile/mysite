# Generated by Django 4.1 on 2025-02-14 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_emailverifyrecord_alter_userprofile_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='charater',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='个性签名'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='desc',
            field=models.TextField(blank=True, default='', max_length=200, verbose_name='个人简介'),
        ),
    ]
