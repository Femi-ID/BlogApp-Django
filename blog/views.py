from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import EmailForm, CommentForm
from django.core.mail import send_mail
# Create your views here.


class PostListView(ListView):
    # an introduction to class-based views at https://docs.djangoproject.com/en/3.0/topics/class-based-views/intro/.
    queryset = Post.published.all()  # another attribute model = Post: Django would have built the generic Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request):
    objects_list = Post.published.all()
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
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month,
                             publish__day=day)

    return render(request, 'blog/post/detail.html', {'post': post})


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
