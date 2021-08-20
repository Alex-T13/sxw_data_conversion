from django.contrib import admin

from applications.reviews.models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'create', 'author', 'edited')
    list_display_links = ('content', )
    search_fields = ('content', )
    list_filter = ('create',)


admin.site.register(Post, PostAdmin)
