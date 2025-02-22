from django.shortcuts import render, get_object_or_404
from .models import Category, Post, Tag
from django.db.models import Q, F
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    # 首页
    post_list = Post.objects.all()  # 查询到所有的文章,queryset
    # 分页方法
    paginator = Paginator(post_list, 4)  # 第二个参数4代表每页显示几个
    page_number = request.GET.get("page")  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "blog/index.html", context)


def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # 获取当前分类下的所有文章
    posts = category.post_set.all()
    paginator = Paginator(posts, 4)  # 第二个参数4代表每页显示几个
    page_number = request.GET.get("page")  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {"category": category, "page_obj": page_obj}
    return render(request, "blog/category_list.html", context)


def post_detail(request, post_id):
    """文章详情"""
    
    post = get_object_or_404(Post, id=post_id)
    Post.objects.filter(id=post_id).update(pv=F("pv") + 1)

    # 通过id获取上一篇文章和下一篇文章
    # prev_post = Post.objects.filter(id__lt=post_id).last()
    # next_post = Post.objects.filter(id__gt=post_id).first()

    # 用发布日期获取上一篇文章和下一篇文章
    prev_post = Post.objects.filter(add_date__lt=post.add_date).last()
    next_post = Post.objects.filter(add_date__gt=post.add_date).first()
    context = {"post": post, "prev_post": prev_post, "next_post": next_post}
    return render(request, "blog/post_detail.html", context)

def search(request):
    """搜索视图"""
    keyword = request.GET.get("keyword")
    # 没有搜索默认显示所有文章
    if not keyword:
        post_list = Post.objects.all()
    else:
        # 包含查询的方法，用Q对象来组合复杂查询，title__icontains 他两个之间用的是双下划线（__）链接
        post_list = Post.objects.filter(
            Q(title__icontains=keyword)
            | Q(desc__icontains=keyword)
            | Q(content__icontains=keyword)
            | Q(category__name__icontains=keyword)
            | Q(tags__name__icontains=keyword)
            | Q(owner__username__icontains=keyword)
        )
    paginator = Paginator(post_list, 4)  # 第二个参数4代表每页显示几个
    page_number = request.GET.get("page")  # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "blog/index.html", context)
