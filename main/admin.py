from django.contrib import admin
from main.models import Source, Feed, UserFeed, Comment, Category


# Register your models here.
class SourceAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("id", "url", "name", "user", "etag", "last_modified", "created_time", "updated_time")


class FeedAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("id", "source", "title", "published_time", "created_time", "updated_time")


class UserFeedAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "id",
        "user",
        "feed", "is_read", "is_bookmarked",
        "is_starred", "created_time", "updated_time"
    )


class CommentAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("id", "user", "feed", "parent", "message", "created_time", "updated_time")


class CategoryAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ("id", "name", "user", "created_time", "updated_time")


admin.site.register(Feed, FeedAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserFeed, UserFeedAdmin)
admin.site.register(Category, CategoryAdmin)
