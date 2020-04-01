from django.contrib import admin

from .models import Key

@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    readonly_fields = ['id']

    def has_change_permission(self, request, obj=None):
        return False
