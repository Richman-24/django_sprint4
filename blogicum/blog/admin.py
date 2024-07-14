from bs4 import Comment
from django.contrib import admin

from blog.models import Category, Location, Post, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ["title", "is_published"]
    list_editable = ["is_published"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "category", "pub_date", "is_published"]
    list_editable = ["is_published", "category"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "author", "created_at", "short_text"]

    def short_text(self, obj):
        return obj.text[:30] + "..." if len(obj.text) > 30 else obj.text
    short_text.short_description = "Text"
