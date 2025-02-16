"""在这里自定义模板标签"""

from django import template
from blog.models import Category, Post, Tag, Sidebar
from django.shortcuts import render

# 注册模板标签
register = template.Library()


@register.simple_tag
def get_category_list():
    # 全站分类
    return Category.objects.all()


@register.simple_tag
def get_sidebar_list():
    # 全站分类
    return Sidebar.get_sidebar()


@register.simple_tag
def get_new_post(num=8):
    """获取最新文章"""
    return Post.objects.all().order_by("-pub_date")[:num]


@register.simple_tag
def get_hot_post(num=8):
    """获取热门文章"""
    return Post.objects.all().order_by("-pv")[:num]
