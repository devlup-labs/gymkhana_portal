from django.contrib import admin
from .models import Event, EventCategory, Festival, SocialLink


class SocialLinkInline(admin.TabularInline):
    model = SocialLink


class FestivalAdmin(admin.ModelAdmin):
    inlines = (SocialLinkInline,)
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'published', 'use_custom_html')
    list_filter = ('published', 'use_custom_html', 'society')
    filter_horizontal = ('society',)

    class Meta:
        model = Festival


class EventInLine(admin.StackedInline):
    model = Event
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('organizers',)


class EventCategoryAdmin(admin.ModelAdmin):
    inlines = (EventInLine,)
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'festival')
    list_filter = ('festival__name',)

    class Meta:
        model = EventCategory


admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Festival, FestivalAdmin)
