from django.contrib import admin

from .models import Blueprint
from sources.models import Source


class SourceInLine(admin.TabularInline):
    model = Source


@admin.register(Blueprint)
class BlueprintAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created')
    list_display = ('id', 'title', 'key', 'created')

    inlines = [
        SourceInLine,
    ]

