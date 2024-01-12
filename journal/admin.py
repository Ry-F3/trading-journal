from django.contrib import admin
from .models import Trade, BlogPost, FAQRequest, Comment, AdminResponse


class TradeAdmin(admin.ModelAdmin):
    list_display = ('display_user', 'id', 'symbol', 'date', 'status', 'long_short', 'position', 'margin', 'leverage', 'open_price', 'current_price', 'return_pnl')
    list_filter = ('user', 'date', 'symbol', 'long_short')
    search_fields = ('symbol', 'position')

    def display_user(self, obj):
        return obj.user.username  # Replace 'username' with the actual attribute of the User model you want to display
    display_user.short_description = 'User'

    def get_queryset(self, request):
        # Show all trades to superusers (admin), and filter by user for regular users
        if request.user.is_superuser:
            return Trade.objects.all()
        else:
            return Trade.objects.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        # Associate the trade with the current user when saving
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        # Only allow users to change their own trades
        if obj is not None and obj.user != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # Only allow users to delete their own trades
        if obj is not None and obj.user != request.user:
            return False
        return super().has_delete_permission(request, obj)


admin.site.register(Trade, TradeAdmin)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_user', 'slug', 'timestamp', 'display_blog_post_likes')
    list_filter = ('user', 'timestamp')
    search_fields = ('title', 'content')

    def display_user(self, obj):
        return obj.user.username
    display_user.short_description = 'Author'

    def display_blog_post_likes(self, obj):
        return obj.likes.count()
    display_blog_post_likes.short_description = 'Likes'

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.user != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.user != request.user:
            return False
        return super().has_delete_permission(request, obj)
        

admin.site.register(BlogPost, BlogPostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'timestamp')
    list_filter = ('user', 'timestamp')
    search_fields = ('content',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if obj is not None and obj.user != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.user != request.user:
            return False
        return super().has_delete_permission(request, obj)
        

admin.site.register(Comment, CommentAdmin)


class AdminResponseInline(admin.TabularInline):
    model = AdminResponse
    extra = 1  # Set the number of empty forms to display
    

@admin.register(FAQRequest)
class FAQRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'title', 'is_approved')
    list_filter = ('user', 'timestamp', 'is_approved')
    search_fields = ('title', 'question')
    inlines = [AdminResponseInline]  # Add the inline for AdminResponse

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser or (obj is not None and obj.user == request.user):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or (obj is not None and obj.user == request.user):
            return True
        return False

        