from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()
# Each module that contains template tags needs to define a variable called register to be a valid tag library

# • simple_tag: Processes the data and returns a string
# • inclusion_tag: Processes the data and returns a rendered template


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}
# Using an inclusion tag, you can render a template with context variables returned by your template tag.


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


"""You can find the list of Django's built-in template filters at https://docs.djangoproject.com/en/3.0/ref/templates/builtins/#built-in-filter-reference
learn the basics of the markdown format at https://daringfireball.net/projects/markdown/basics."""

# CUSTOM TEMPLATE FILTERS
# more information about custom filters (how to customize your template filter) at
# https://docs.djangoproject.com/en/3.0/howto/custom-templatetags/#writing-custom-template-filters.

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
# By default, Django will not trust any HTML code and will escape it before placing it in the output.
# The only exceptions are variables that are marked as safe from escaping.
# This behavior prevents Django from outputting potentially dangerous HTML
# and allows you to create exceptions for returning safe HTML.


