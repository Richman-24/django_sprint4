from django.contrib import admin

from blog.models import Category, Location, Post


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
