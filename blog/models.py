from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# You can take a look at all the possible options at:
# https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.
# Different types of fields that you can use to define your models:
# https://docs.djangoproject.com/en/3.0/ref/models/fields/


class PublishedManager(models.Manager):
    def get_queryset(self):
        # To create a custom manager to retrieve all posts with the published status.
        return super(PublishedManager, self).get_queryset().filter(status='published')
        # The get_queryset() method of a manager returns the QuerySet that will be
        # executed. You override this method to include your custom filter in the final QuerySet.


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)  # returns the current datetime in a timezone-aware format.
    created = models.DateTimeField(auto_now_add=True)  # auto_now_add: the date will be saved automatically
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()  # The default manager
    published = PublishedManager()  # Our custom manager
    # The first manager declared in a model becomes the default manager.
    # default_manager_name -to specify a different default manager.

    class Meta:
        ordering = ('-publish',)

    def __repr__(self):
        return f'title: {self.title}, author: {self.author}'

    # Canonical URLS for models
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month,
                                                 self.publish.day, self.slug])

    tags = TaggableManager()


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # The related_name attribute allows you to name the attribute that you use for the relationship from the related object back to this one.
    # After defining this, you can retrieve the post of a comment object using comment.post and retrieve all comments of a post using post.comments.all().
    # learn more about many-to-one relationships: https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_one/.
    name = models.CharField(max_length=70)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
