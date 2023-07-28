from django.contrib import admin
from .models import Post, Comments


# Register your models here.

# admin.site.register(Post)

@admin.register(Post)  # performs the same function as the admin.site.register() function
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created')
    list_filter = ('email', 'active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')




