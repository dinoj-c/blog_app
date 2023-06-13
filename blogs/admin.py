from django.contrib import admin
from blogs.models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BlogPost._meta.fields]
    exclude = ('auto_id', 'creator', 'updater', 'is_deleted')
    list_filter = ('is_deleted',)

admin.site.register(BlogPost, BlogPostAdmin)
