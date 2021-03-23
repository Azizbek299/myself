from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import Category, Post, Tag

'''
def index(request):
    page_obj = Post.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(page_obj, 2)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    posts = Post.objects.all()
    cate = Category.objects.all()
    return render(request, 'blog/home.html', {'page_obj': page_obj, 'posts': posts, 'categories': cate})


def category(request, title):
    cate = Category.objects.all()
    categories = Category.objects.get(title=title)
    posts = Post.objects.filter(category=categories)
    return render(request, 'blog/category.html', {'posts': posts, 'categories': cate})
'''


class HomeListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'blog/index.html'
    paginate_by = 4

    # def get_context_data(self, **kwargs):
    #     context = super(HomeListView, self).get_context_data(**kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context


class CategoryList(ListView):
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # get(slug=self.kwargs['slug'])
        return context

    # def get_queryset(self):
    #   categories = get_object_or_404(Category, title=self.kwargs.get('title'))
    #   return Post.objects.filter(category=categories)

    # def get_context_data(self, **kwargs):
    #   context = super(CategoryList, self).get_context_data(**kwargs)
    #   categories = get_object_or_404(Category, title=self.kwargs.get('title'))
    #   context['posts'] = Post.objects.filter(category=categories)
    #   context['categories'] = Category.objects.all()
    #   return context


class PostDetail(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.filter(slug=self.kwargs['slug'])
        context['taglar'] = Tag.objects.all()
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class TagView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 2
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class SearchView(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context
