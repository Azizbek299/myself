from django import template
from blog.models import Post, Tag, Category
from django.db.models import Count
register = template.Library()


@register.inclusion_tag('blog/popular_post_tpl.html')
def get_popular(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt]
    return {'posts': posts}


@register.simple_tag()
def get_categories():
    return Category.objects.annotate(cnt=Count('posts')).filter(cnt__gt=0).order_by('id')
