from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import EmailForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector
# Create your views here.
"""Always make sure u don't make changes after committing and pushing changes to 'master'
(when you're still on the master branch) with the mindset of switching branches.
make sure the last thing you do before leaving a branch to work on another is to: (add file and commit file)"""


class PostListView(ListView):
    # an introduction to class-based views at https://docs.djangoproject.com/en/3.0/topics/class-based-views/intro/.
    queryset = Post.published.all()  # another attribute model = Post: Django would have built the generic Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    objects_list = Post.published.all()
    tag = None

    # let users list all posts tagged with a specific tag.
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Since this is a many-to-many relationship, you filter posts by tags contained in a given list.
        objects_list = objects_list.filter(tags__in=[tag])

    paginator = Paginator(objects_list, 3)  # 3 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver the last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)

    # List of active comments for this post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save.
            # The save() method creates an instance of the model that the form is linked to
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    # djangotaggit also includes a similar_objects() manager that you can use to retrieve objects by shared tags.
    # Take a look at all django-taggit managers at https://django-taggit.readthedocs.io/en/latest/api.html.
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts})


def post_share(request, post_id):
    # To retrieve by id
    post = get_object_or_404(Post, id=post_id)
    sent = False

    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():  # list of validation errors by accessing form.errors.
            form_clean = form.cleaned_data  # if form is validated and cleaned
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{form_clean['name']} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n " \
                      f"{form_clean['name']}'s comments: {form_clean['comment']}"
            send_mail(subject, message, 'django@blog.com', [form_clean['to']])
            sent = True  # to be used to display success message upon successful submission.
    else:
        form = EmailForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

# The send_mail() function takes the subject, message, sender, and list of recipients as required arguments.
# from django.core.mail import mail: send_mail('', '', '', [])



