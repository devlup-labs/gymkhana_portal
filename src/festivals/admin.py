from django.contrib import admin
from .models import FestivalEvent, FestivalEventCategory, Festival


class FestivalEventInLine(admin.StackedInline):
    model = FestivalEvent
    prepopulated_fields = {"slug": ("name",)}


class EventCategoryAdmin(admin.ModelAdmin):
    inlines = (FestivalEventInLine,)
    prepopulated_fields = {"slug": ("name",)}
    list_display = ['name', 'festival']
    list_filter = ['festival__name', ]

    class Meta:
        model = FestivalEventCategory


admin.site.register(FestivalEventCategory, EventCategoryAdmin)
admin.site.register(Festival)
