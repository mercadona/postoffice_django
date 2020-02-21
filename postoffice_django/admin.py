from django.contrib import admin

from .models import PublishingError


@admin.register(PublishingError)
class PublishingErrorAdmin(admin.ModelAdmin):

    list_display = ['topic', 'error', 'created_at']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
