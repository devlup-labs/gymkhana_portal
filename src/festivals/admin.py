from django.contrib import admin
from .models import Event, EventCategory, Festival


class FestivalAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'published', 'default_html')
    list_filter = ('published', 'default_html')

    class Meta:
        model = Festival


class EventInLine(admin.StackedInline):
    model = Event
    prepopulated_fields = {"slug": ("name",)}


class EventCategoryAdmin(admin.ModelAdmin):
    inlines = (EventInLine,)
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'festival')
    list_filter = ('festival__name', )

    class Meta:
        model = EventCategory


admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Festival, FestivalAdmin)
