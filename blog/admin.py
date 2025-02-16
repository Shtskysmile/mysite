from django.contrib import admin
from .models import Category, Post, Tag, Sidebar

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Sidebar)


class PostAdmin(admin.ModelAdmin):
    """文章详情管理"""
    # 显示的字段
    list_display = (
        "id",
        "title",
        "category",
        "tags",
        "owner",
        "pv",
        "pub_date",
    )

    # 过滤器
    list_filter = ("owner",)
    # 搜索字段
    search_fields = ("title", "desc")
    # 可以点击到编辑页面去
    list_display_links = (
        "id",
        "title",
    )

    class Media:
        css = {"all": ("ckeditor5/cked.css",)}

        js = (
            "js/jquery.js",
            "ckeditor5/ckeditor.js",
            "ckeditor5/translations/zh.js",
            "ckeditor5/config.js",
        )

admin.site.register(Post, PostAdmin)
