from django.contrib import admin
from .models import Post, Category, Comment
from django.utils.html import strip_tags


class CommentInline(admin.TabularInline):  # 也可以用 admin.StackedInline
    model = Comment
    extra = 1  # 顯示一個可新增的空白欄位
    fields = ("user", "content", "created_at")
    readonly_fields = ("created_at",)


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 列表顯示的欄位
    list_display = (
        "id",
        "title",
        "author",
        "short_body",
        "created_at",
        "image",
        "category",
    )

    # 可以搜尋的欄位
    search_fields = ("title", "author__username", "body")

    # 可用於篩選的欄位
    list_filter = (
        "author",
        "category",
    )

    inlines = [CommentInline]

    # 自訂顯示 body 的縮略文字
    def short_body(self, obj):
        text = strip_tags(obj.body)
        return text[:50] + "…" if len(text) > 50 else text

    short_body.short_description = "Body Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "post",
        "user",
        "short_content",
        "parent",
        "created_at",
    )
    search_fields = ("post__title", "user__username", "content")
    list_filter = ("user", "created_at")

    def short_content(self, obj):
        text = strip_tags(obj.content)
        return text[:50] + "…" if len(text) > 50 else text

    short_content.short_description = "Content Preview"
